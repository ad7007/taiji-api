import json
import threading
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from loguru import logger
import hashlib

class StateStore:
    def __init__(self, storage_path: str = "state.json"):
        self.storage_path = storage_path
        self.state = self._load_state()
    
    def _load_state(self) -> Dict[str, Any]:
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"nodes": {}, "edges": {}, "metadata": {}}
    
    def save_state(self, state: Dict[str, Any]):
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

class BackupStore:
    def __init__(self, backup_dir: str = "backups"):
        import os
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, state: Dict[str, Any]):
        import os
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            logger.info(f"Created backup: {backup_path}")
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")

class Task:
    def __init__(self, task_id: str, action: str, params: Dict[str, Any], priority: int = 0):
        self.task_id = task_id
        self.action = action
        self.params = params
        self.priority = priority
        self.created_at = time.time()
        self.status = "pending"

class TaskManager:
    def __init__(self, max_threads: int = 4):
        self.tasks: List[Task] = []
        self.task_lock = threading.Lock()
        self.thread_pool = []
        self.max_threads = max_threads
        self.running = True
        self._start_workers()
    
    def _start_workers(self):
        for _ in range(self.max_threads):
            thread = threading.Thread(target=self._worker, daemon=True)
            thread.start()
            self.thread_pool.append(thread)
    
    def _worker(self):
        while self.running:
            task = self._get_next_task()
            if task:
                self._execute_task(task)
            time.sleep(0.1)
    
    def _get_next_task(self) -> Optional[Task]:
        with self.task_lock:
            if not self.tasks:
                return None
            self.tasks.sort(key=lambda t: t.priority, reverse=True)
            task = self.tasks.pop(0)
            task.status = "running"
            return task
    
    def _execute_task(self, task: Task):
        try:
            logger.info(f"Executing task: {task.task_id} - {task.action}")
            time.sleep(0.5)  # Simulate work
            task.status = "completed"
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            task.status = "failed"
    
    def add_task(self, action: str, params: Dict[str, Any], priority: int = 0) -> str:
        task_id = hashlib.md5(f"{action}_{time.time()}".encode()).hexdigest()
        task = Task(task_id, action, params, priority)
        with self.task_lock:
            self.tasks.append(task)
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[str]:
        with self.task_lock:
            for task in self.tasks:
                if task.task_id == task_id:
                    return task.status
            return None

class Event:
    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.event_type = event_type
        self.data = data
        self.timestamp = time.time()

class EventManager:
    def __init__(self):
        self.listeners = {}
        self.event_lock = threading.Lock()
    
    def subscribe(self, event_type: str, callback):
        with self.event_lock:
            if event_type not in self.listeners:
                self.listeners[event_type] = []
            self.listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback):
        with self.event_lock:
            if event_type in self.listeners:
                self.listeners[event_type].remove(callback)
    
    def emit(self, event_type: str, data: Dict[str, Any]):
        event = Event(event_type, data)
        with self.event_lock:
            if event_type in self.listeners:
                for callback in self.listeners[event_type]:
                    try:
                        callback(event)
                    except Exception as e:
                        logger.error(f"Error in event callback: {e}")

class TaijiManager:
    def __init__(self):
        self.state_store = StateStore()
        self.backup_store = BackupStore()
        self.task_manager = TaskManager()
        self.event_manager = EventManager()
        self.lock = threading.RLock()
        self.cache = {}
        self.cache_expiry = {}
        self.cache_ttl = 300  # 5 minutes
        self.initialize_system()
    
    def initialize_system(self):
        logger.info("Initializing Taiji system...")
        self._load_initial_state()
        logger.info("Taiji system initialized successfully")
    
    def _load_initial_state(self):
        initial_state = {
            "nodes": {
                "yin": {"type": "yin", "value": 0.5, "connections": ["yang"]},
                "yang": {"type": "yang", "value": 0.5, "connections": ["yin"]}
            },
            "edges": {
                "yin-yang": {"source": "yin", "target": "yang", "strength": 0.8}
            },
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "version": "1.0.0"
            }
        }
        
        current_state = self.state_store.state
        if not current_state["nodes"]:
            self.state_store.save_state(initial_state)
            self.state_store.state = initial_state
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        if key in self.cache:
            if time.time() < self.cache_expiry.get(key, 0):
                return self.cache[key]
            else:
                del self.cache[key]
                del self.cache_expiry[key]
        return None
    
    def _set_cache(self, key: str, value: Any):
        self.cache[key] = value
        self.cache_expiry[key] = time.time() + self.cache_ttl
    
    def get_state(self) -> Dict[str, Any]:
        cache_key = "state"
        cached_state = self._get_from_cache(cache_key)
        if cached_state:
            return cached_state
        
        with self.lock:
            state = self.state_store.state
            self._set_cache(cache_key, state)
            return state
    
    def perform_zhengzhuan(self, node_id: str, value: float) -> Dict[str, Any]:
        if not 0 <= value <= 1:
            raise ValueError("Value must be between 0 and 1")
        
        task_id = self.task_manager.add_task("zhengzhuan", {"node_id": node_id, "value": value}, priority=1)
        
        with self.lock:
            state = self.state_store.state
            if node_id in state["nodes"]:
                state["nodes"][node_id]["value"] = value
                state["metadata"]["last_updated"] = datetime.now().isoformat()
                
                # Create backup
                self.backup_store.create_backup(state)
                
                # Save state
                self.state_store.save_state(state)
                
                # Clear cache
                self.cache.clear()
                
                # Emit event
                self.event_manager.emit("state_updated", {"node_id": node_id, "action": "zhengzhuan"})
                
                return {
                    "success": True,
                    "message": f"Performed zhengzhuan on node {node_id}",
                    "task_id": task_id
                }
            else:
                return {
                    "success": False,
                    "message": f"Node {node_id} not found"
                }
    
    def perform_fanzhuan(self, node_id: str) -> Dict[str, Any]:
        task_id = self.task_manager.add_task("fanzhuan", {"node_id": node_id}, priority=1)
        
        with self.lock:
            state = self.state_store.state
            if node_id in state["nodes"]:
                current_value = state["nodes"][node_id]["value"]
                state["nodes"][node_id]["value"] = 1.0 - current_value
                state["metadata"]["last_updated"] = datetime.now().isoformat()
                
                # Create backup
                self.backup_store.create_backup(state)
                
                # Save state
                self.state_store.save_state(state)
                
                # Clear cache
                self.cache.clear()
                
                # Emit event
                self.event_manager.emit("state_updated", {"node_id": node_id, "action": "fanzhuan"})
                
                return {
                    "success": True,
                    "message": f"Performed fanzhuan on node {node_id}",
                    "task_id": task_id
                }
            else:
                return {
                    "success": False,
                    "message": f"Node {node_id} not found"
                }
    
    def reset_state(self) -> Dict[str, Any]:
        task_id = self.task_manager.add_task("reset_state", {}, priority=2)
        
        with self.lock:
            initial_state = {
                "nodes": {
                    "yin": {"type": "yin", "value": 0.5, "connections": ["yang"]},
                    "yang": {"type": "yang", "value": 0.5, "connections": ["yin"]}
                },
                "edges": {
                    "yin-yang": {"source": "yin", "target": "yang", "strength": 0.8}
                },
                "metadata": {
                    "last_updated": datetime.now().isoformat(),
                    "version": "1.0.0"
                }
            }
            
            # Create backup before reset
            self.backup_store.create_backup(self.state_store.state)
            
        # Save state outside the lock to avoid deadlock
        self.state_store.save_state(initial_state)
        self.state_store.state = initial_state
        
        # Clear cache
        self.cache.clear()
        
        # Emit event
        self.event_manager.emit("state_reset", {})
        
        return {
            "success": True,
            "message": "State reset to initial values",
            "task_id": task_id
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        cache_key = "statistics"
        cached_stats = self._get_from_cache(cache_key)
        if cached_stats:
            return cached_stats
        
        with self.lock:
            state = self.state_store.state
            stats = {
                "node_count": len(state["nodes"]),
                "edge_count": len(state["edges"]),
                "last_updated": state["metadata"].get("last_updated"),
                "version": state["metadata"].get("version")
            }
            self._set_cache(cache_key, stats)
            return stats
    
    def add_node(self, node_id: str, node_type: str, initial_value: float = 0.5) -> Dict[str, Any]:
        if not 0 <= initial_value <= 1:
            raise ValueError("Initial value must be between 0 and 1")
        
        task_id = self.task_manager.add_task("add_node", {"node_id": node_id, "node_type": node_type, "initial_value": initial_value})
        
        with self.lock:
            state = self.state_store.state
            if node_id not in state["nodes"]:
                state["nodes"][node_id] = {
                    "type": node_type,
                    "value": initial_value,
                    "connections": []
                }
                state["metadata"]["last_updated"] = datetime.now().isoformat()
                
                # Create backup
                self.backup_store.create_backup(state)
                
                # Save state
                self.state_store.save_state(state)
                
                # Clear cache
                self.cache.clear()
                
                # Emit event
                self.event_manager.emit("node_added", {"node_id": node_id, "node_type": node_type})
                
                return {
                    "success": True,
                    "message": f"Added node {node_id} of type {node_type}",
                    "task_id": task_id
                }
            else:
                return {
                    "success": False,
                    "message": f"Node {node_id} already exists"
                }
    
    def remove_node(self, node_id: str) -> Dict[str, Any]:
        task_id = self.task_manager.add_task("remove_node", {"node_id": node_id})
        
        with self.lock:
            state = self.state_store.state
            if node_id in state["nodes"]:
                # Remove node
                del state["nodes"][node_id]
                
                # Remove edges connected to this node
                edges_to_remove = []
                for edge_id, edge in state["edges"].items():
                    if edge["source"] == node_id or edge["target"] == node_id:
                        edges_to_remove.append(edge_id)
                
                for edge_id in edges_to_remove:
                    del state["edges"][edge_id]
                
                # Update connections in other nodes
                for other_node_id, other_node in state["nodes"].items():
                    if node_id in other_node["connections"]:
                        other_node["connections"].remove(node_id)
                
                state["metadata"]["last_updated"] = datetime.now().isoformat()
                
                # Create backup
                self.backup_store.create_backup(state)
                
                # Save state
                self.state_store.save_state(state)
                
                # Clear cache
                self.cache.clear()
                
                # Emit event
                self.event_manager.emit("node_removed", {"node_id": node_id})
                
                return {
                    "success": True,
                    "message": f"Removed node {node_id}",
                    "task_id": task_id
                }
            else:
                return {
                    "success": False,
                    "message": f"Node {node_id} not found"
                }
    
    def add_edge(self, edge_id: str, source: str, target: str, strength: float = 0.5) -> Dict[str, Any]:
        if not 0 <= strength <= 1:
            raise ValueError("Strength must be between 0 and 1")
        
        task_id = self.task_manager.add_task("add_edge", {"edge_id": edge_id, "source": source, "target": target, "strength": strength})
        
        with self.lock:
            state = self.state_store.state
            if source in state["nodes"] and target in state["nodes"]:
                if edge_id not in state["edges"]:
                    state["edges"][edge_id] = {
                        "source": source,
                        "target": target,
                        "strength": strength
                    }
                    
                    # Update connections in nodes
                    if target not in state["nodes"][source]["connections"]:
                        state["nodes"][source]["connections"].append(target)
                    if source not in state["nodes"][target]["connections"]:
                        state["nodes"][target]["connections"].append(source)
                    
                    state["metadata"]["last_updated"] = datetime.now().isoformat()
                    
                    # Create backup
                    self.backup_store.create_backup(state)
                    
                    # Save state
                    self.state_store.save_state(state)
                    
                    # Clear cache
                    self.cache.clear()
                    
                    # Emit event
                    self.event_manager.emit("edge_added", {"edge_id": edge_id, "source": source, "target": target})
                    
                    return {
                        "success": True,
                        "message": f"Added edge {edge_id} between {source} and {target}",
                        "task_id": task_id
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Edge {edge_id} already exists"
                    }
            else:
                return {
                    "success": False,
                    "message": "Source or target node not found"
                }
    
    def remove_edge(self, edge_id: str) -> Dict[str, Any]:
        task_id = self.task_manager.add_task("remove_edge", {"edge_id": edge_id})
        
        with self.lock:
            state = self.state_store.state
            if edge_id in state["edges"]:
                edge = state["edges"][edge_id]
                source = edge["source"]
                target = edge["target"]
                
                # Remove edge
                del state["edges"][edge_id]
                
                # Update connections in nodes
                if target in state["nodes"][source]["connections"]:
                    state["nodes"][source]["connections"].remove(target)
                if source in state["nodes"][target]["connections"]:
                    state["nodes"][target]["connections"].remove(source)
                
                state["metadata"]["last_updated"] = datetime.now().isoformat()
                
                # Create backup
                self.backup_store.create_backup(state)
                
                # Save state
                self.state_store.save_state(state)
                
                # Clear cache
                self.cache.clear()
                
                # Emit event
                self.event_manager.emit("edge_removed", {"edge_id": edge_id})
                
                return {
                    "success": True,
                    "message": f"Removed edge {edge_id}",
                    "task_id": task_id
                }
            else:
                return {
                    "success": False,
                    "message": f"Edge {edge_id} not found"
                }

if __name__ == "__main__":
    taiji = TaijiManager()
    print("Taiji system initialized")
    print("Current state:", taiji.get_state())
    
    # Test zhengzhuan
    result = taiji.perform_zhengzhuan("yin", 0.8)
    print("Zhengzhuan result:", result)
    print("State after zhengzhuan:", taiji.get_state())
    
    # Test fanzhuan
    result = taiji.perform_fanzhuan("yang")
    print("Fanzhuan result:", result)
    print("State after fanzhuan:", taiji.get_state())
    
    # Test reset
    result = taiji.reset_state()
    print("Reset result:", result)
    print("State after reset:", taiji.get_state())
    
    # Test statistics
    stats = taiji.get_statistics()
    print("Statistics:", stats)
