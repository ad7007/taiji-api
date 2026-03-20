"""
太极管控体系 - 核心实现

包含：
- RBAC 角色权限控制
- 审批流程（红灯确认）
- 审计日志
- 权限等级（L0-L4）
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import os

# ==================== 枚举定义 ====================

class PermissionLevel(Enum):
    """权限等级"""
    L0_FORBIDDEN = 0      # 完全禁止
    L1_APPROVAL = 1       # 人工审批
    L2_NOTIFY = 2         # 通知确认
    L3_AUTO = 3           # 自动执行（米珞）
    L4_AUTONOMOUS = 4     # 完全自主（8宫）


class Role(Enum):
    """角色类型"""
    COMMANDER = "commander"    # 主控（5宫）
    WORKER = "worker"          # 执行者（1,2,3,4,6,8,9宫）
    VALIDATOR = "validator"    # 验收者（7宫）


class RiskLevel(Enum):
    """风险等级"""
    CRITICAL = "critical"      # 极高（L0）
    HIGH = "high"              # 高（L1）
    MEDIUM = "medium"          # 中（L2）
    LOW = "low"                # 低（L3）
    MINIMAL = "minimal"        # 极低（L4）


class OperationType(Enum):
    """操作类型"""
    # L0 级别
    DELETE_PALACE = "delete_palace"
    EXTERNAL_SEND = "external_send"
    FINANCIAL_OPERATION = "financial_operation"
    
    # L1 级别
    PUBLISH_CONTENT = "publish_content"
    INSTALL_SKILL = "install_skill"
    MODIFY_CONFIG = "modify_config"
    
    # L2 级别
    COMMIT_CODE = "commit_code"
    QUALITY_REPORT = "quality_report"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    
    # L3 级别
    DATA_COLLECTION = "data_collection"
    TASK_DISPATCH = "task_dispatch"
    STATUS_REPORT = "status_report"
    
    # L4 级别
    MONITORING = "monitoring"
    LOG_SYNC = "log_sync"
    AUTO_BACKUP = "auto_backup"


# ==================== 数据类 ====================

@dataclass
class Permission:
    """权限定义"""
    name: str
    description: str
    level: PermissionLevel
    

@dataclass
class RolePermissions:
    """角色权限集合"""
    role: Role
    permissions: List[str]
    default_level: PermissionLevel


@dataclass
class AuditLog:
    """审计日志"""
    timestamp: str
    session_id: str
    palace: int
    action: str
    target_palace: Optional[int]
    task_type: str
    permission_level: str
    risk_level: str
    result: str
    duration_ms: int
    user_instruction: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "session_id": self.session_id,
            "palace": self.palace,
            "action": self.action,
            "target_palace": self.target_palace,
            "task_type": self.task_type,
            "permission_level": self.permission_level,
            "risk_level": self.risk_level,
            "result": self.result,
            "duration_ms": self.duration_ms,
            "user_instruction": self.user_instruction
        }


# ==================== RBAC 权限控制 ====================

class RBACManager:
    """RBAC 权限管理器"""
    
    # 角色权限定义
    ROLE_PERMISSIONS: Dict[Role, RolePermissions] = {
        Role.COMMANDER: RolePermissions(
            role=Role.COMMANDER,
            permissions=["dispatch", "coordinate", "monitor", "report", "approve"],
            default_level=PermissionLevel.L3_AUTO
        ),
        Role.WORKER: RolePermissions(
            role=Role.WORKER,
            permissions=["execute", "report"],
            default_level=PermissionLevel.L4_AUTONOMOUS
        ),
        Role.VALIDATOR: RolePermissions(
            role=Role.VALIDATOR,
            permissions=["validate", "audit", "approve", "reject"],
            default_level=PermissionLevel.L1_APPROVAL
        )
    }
    
    # 宫位角色映射
    PALACE_ROLES: Dict[int, Role] = {
        1: Role.WORKER,
        2: Role.WORKER,
        3: Role.WORKER,
        4: Role.WORKER,
        5: Role.COMMANDER,
        6: Role.WORKER,
        7: Role.VALIDATOR,
        8: Role.WORKER,
        9: Role.WORKER
    }
    
    # 宫位默认权限
    PALACE_DEFAULT_LEVEL: Dict[int, PermissionLevel] = {
        1: PermissionLevel.L3_AUTO,
        2: PermissionLevel.L2_NOTIFY,
        3: PermissionLevel.L2_NOTIFY,
        4: PermissionLevel.L2_NOTIFY,
        5: PermissionLevel.L3_AUTO,
        6: PermissionLevel.L4_AUTONOMOUS,
        7: PermissionLevel.L1_APPROVAL,
        8: PermissionLevel.L2_NOTIFY,
        9: PermissionLevel.L3_AUTO
    }
    
    @classmethod
    def get_role(cls, palace_id: int) -> Role:
        """获取宫位角色"""
        return cls.PALACE_ROLES.get(palace_id, Role.WORKER)
    
    @classmethod
    def get_permissions(cls, palace_id: int) -> List[str]:
        """获取宫位权限列表"""
        role = cls.get_role(palace_id)
        return cls.ROLE_PERMISSIONS[role].permissions
    
    @classmethod
    def get_default_level(cls, palace_id: int) -> PermissionLevel:
        """获取宫位默认权限等级"""
        return cls.PALACE_DEFAULT_LEVEL.get(palace_id, PermissionLevel.L2_NOTIFY)
    
    @classmethod
    def has_permission(cls, palace_id: int, permission: str) -> bool:
        """检查宫位是否有某权限"""
        permissions = cls.get_permissions(palace_id)
        return permission in permissions


# ==================== 审批系统 ====================

class ApprovalStatus(Enum):
    """审批状态"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    TIMEOUT = "timeout"


@dataclass
class ApprovalRequest:
    """审批请求"""
    request_id: str
    palace_id: int
    operation: OperationType
    risk_level: RiskLevel
    status: ApprovalStatus
    created_at: str
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    reason: Optional[str] = None


class ApprovalManager:
    """审批管理器"""
    
    def __init__(self, storage_path: str = "/tmp/taiji_approvals.json"):
        self.storage_path = storage_path
        self.pending_requests: Dict[str, ApprovalRequest] = {}
        self._load()
    
    def _load(self):
        """加载待审批请求"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for k, v in data.items():
                    self.pending_requests[k] = ApprovalRequest(**v)
    
    def _save(self):
        """保存待审批请求"""
        with open(self.storage_path, 'w') as f:
            data = {}
            for k, v in self.pending_requests.items():
                item = {
                    "request_id": v.request_id,
                    "palace_id": v.palace_id,
                    "operation": v.operation.value,
                    "risk_level": v.risk_level.value,
                    "status": v.status.value,
                    "created_at": v.created_at,
                    "approved_by": v.approved_by,
                    "approved_at": v.approved_at,
                    "reason": v.reason
                }
                data[k] = item
            json.dump(data, f)
    
    def create_request(self, palace_id: int, operation: OperationType) -> ApprovalRequest:
        """创建审批请求"""
        request_id = f"apr_{datetime.now().strftime('%Y%m%d%H%M%S')}_{palace_id}"
        risk_level = self._get_risk_level(operation)
        
        request = ApprovalRequest(
            request_id=request_id,
            palace_id=palace_id,
            operation=operation,
            risk_level=risk_level,
            status=ApprovalStatus.PENDING,
            created_at=datetime.now().isoformat()
        )
        
        self.pending_requests[request_id] = request
        self._save()
        return request
    
    def approve(self, request_id: str, approved_by: str, reason: str = "") -> bool:
        """批准请求"""
        if request_id not in self.pending_requests:
            return False
        
        request = self.pending_requests[request_id]
        request.status = ApprovalStatus.APPROVED
        request.approved_by = approved_by
        request.approved_at = datetime.now().isoformat()
        request.reason = reason
        
        self._save()
        return True
    
    def reject(self, request_id: str, reason: str) -> bool:
        """拒绝请求"""
        if request_id not in self.pending_requests:
            return False
        
        request = self.pending_requests[request_id]
        request.status = ApprovalStatus.REJECTED
        request.reason = reason
        
        self._save()
        return True
    
    def get_pending(self) -> List[ApprovalRequest]:
        """获取所有待审批请求"""
        return [r for r in self.pending_requests.values() 
                if r.status == ApprovalStatus.PENDING]
    
    @staticmethod
    def _get_risk_level(operation: OperationType) -> RiskLevel:
        """根据操作类型判断风险等级"""
        risk_mapping = {
            # L0
            OperationType.DELETE_PALACE: RiskLevel.CRITICAL,
            OperationType.EXTERNAL_SEND: RiskLevel.CRITICAL,
            OperationType.FINANCIAL_OPERATION: RiskLevel.CRITICAL,
            # L1
            OperationType.PUBLISH_CONTENT: RiskLevel.HIGH,
            OperationType.INSTALL_SKILL: RiskLevel.HIGH,
            OperationType.MODIFY_CONFIG: RiskLevel.HIGH,
            # L2
            OperationType.COMMIT_CODE: RiskLevel.MEDIUM,
            OperationType.QUALITY_REPORT: RiskLevel.MEDIUM,
            OperationType.COMPETITOR_ANALYSIS: RiskLevel.MEDIUM,
            # L3
            OperationType.DATA_COLLECTION: RiskLevel.LOW,
            OperationType.TASK_DISPATCH: RiskLevel.LOW,
            OperationType.STATUS_REPORT: RiskLevel.LOW,
            # L4
            OperationType.MONITORING: RiskLevel.MINIMAL,
            OperationType.LOG_SYNC: RiskLevel.MINIMAL,
            OperationType.AUTO_BACKUP: RiskLevel.MINIMAL,
        }
        return risk_mapping.get(operation, RiskLevel.MEDIUM)


# ==================== 审计系统 ====================

class AuditManager:
    """审计管理器"""
    
    def __init__(self, log_path: str = "/tmp/taiji_audit.log"):
        self.log_path = log_path
    
    def log(self, 
            session_id: str,
            palace: int,
            action: str,
            task_type: str,
            result: str,
            duration_ms: int,
            user_instruction: str,
            target_palace: Optional[int] = None,
            permission_level: PermissionLevel = PermissionLevel.L3_AUTO,
            risk_level: RiskLevel = RiskLevel.LOW) -> AuditLog:
        """记录审计日志"""
        
        log_entry = AuditLog(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            palace=palace,
            action=action,
            target_palace=target_palace,
            task_type=task_type,
            permission_level=permission_level.name,
            risk_level=risk_level.value,
            result=result,
            duration_ms=duration_ms,
            user_instruction=user_instruction
        )
        
        # 追加到日志文件
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(log_entry.to_dict()) + '\n')
        
        return log_entry
    
    def query(self, 
              palace: Optional[int] = None,
              level: Optional[str] = None,
              result: Optional[str] = None,
              days: int = 7) -> List[Dict[str, Any]]:
        """查询审计日志"""
        logs = []
        
        if not os.path.exists(self.log_path):
            return logs
        
        cutoff = datetime.now().timestamp() - (days * 86400)
        
        with open(self.log_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    
                    # 过滤条件
                    if palace and entry.get('palace') != palace:
                        continue
                    if level and entry.get('permission_level') != level:
                        continue
                    if result and entry.get('result') != result:
                        continue
                    
                    # 时间过滤
                    ts = datetime.fromisoformat(entry['timestamp']).timestamp()
                    if ts < cutoff:
                        continue
                    
                    logs.append(entry)
                except:
                    continue
        
        return logs


# ==================== 权限检查 ====================

class PermissionChecker:
    """权限检查器"""
    
    # 操作与权限等级映射
    OPERATION_LEVELS: Dict[OperationType, PermissionLevel] = {
        # L0
        OperationType.DELETE_PALACE: PermissionLevel.L0_FORBIDDEN,
        OperationType.EXTERNAL_SEND: PermissionLevel.L0_FORBIDDEN,
        OperationType.FINANCIAL_OPERATION: PermissionLevel.L0_FORBIDDEN,
        # L1
        OperationType.PUBLISH_CONTENT: PermissionLevel.L1_APPROVAL,
        OperationType.INSTALL_SKILL: PermissionLevel.L1_APPROVAL,
        OperationType.MODIFY_CONFIG: PermissionLevel.L1_APPROVAL,
        # L2
        OperationType.COMMIT_CODE: PermissionLevel.L2_NOTIFY,
        OperationType.QUALITY_REPORT: PermissionLevel.L2_NOTIFY,
        OperationType.COMPETITOR_ANALYSIS: PermissionLevel.L2_NOTIFY,
        # L3
        OperationType.DATA_COLLECTION: PermissionLevel.L3_AUTO,
        OperationType.TASK_DISPATCH: PermissionLevel.L3_AUTO,
        OperationType.STATUS_REPORT: PermissionLevel.L3_AUTO,
        # L4
        OperationType.MONITORING: PermissionLevel.L4_AUTONOMOUS,
        OperationType.LOG_SYNC: PermissionLevel.L4_AUTONOMOUS,
        OperationType.AUTO_BACKUP: PermissionLevel.L4_AUTONOMOUS,
    }
    
    @classmethod
    def can_execute(cls, 
                    palace_id: int, 
                    operation: OperationType,
                    current_level: Optional[PermissionLevel] = None) -> tuple[bool, str]:
        """
        检查是否可以执行操作
        
        返回: (can_execute, reason)
        """
        required_level = cls.OPERATION_LEVELS.get(operation, PermissionLevel.L2_NOTIFY)
        
        if current_level is None:
            current_level = RBACManager.get_default_level(palace_id)
        
        # L0 永远禁止，需要余总审批
        if required_level == PermissionLevel.L0_FORBIDDEN:
            return False, f"操作 {operation.value} 被禁止，需要余总审批"
        
        # 检查当前权限是否足够
        if current_level.value >= required_level.value:
            return True, "权限充足"
        
        return False, f"权限不足，需要 {required_level.name}，当前 {current_level.name}"
    
    @classmethod
    def get_required_level(cls, operation: OperationType) -> PermissionLevel:
        """获取操作所需权限等级"""
        return cls.OPERATION_LEVELS.get(operation, PermissionLevel.L2_NOTIFY)


# ==================== 权限升降级 ====================

class PermissionManager:
    """权限管理器 - 处理升降级"""
    
    def __init__(self, storage_path: str = "/tmp/taiji_permission_stats.json"):
        self.storage_path = storage_path
        self.stats: Dict[int, Dict[str, Any]] = {}
        self._load()
    
    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                self.stats = json.load(f)
    
    def _save(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.stats, f)
    
    def record_execution(self, palace_id: int, success: bool):
        """记录执行结果"""
        if palace_id not in self.stats:
            self.stats[palace_id] = {
                "total": 0,
                "success": 0,
                "failed": 0,
                "validation_passed": 0,
                "current_level": RBACManager.get_default_level(palace_id).value
            }
        
        self.stats[palace_id]["total"] += 1
        if success:
            self.stats[palace_id]["success"] += 1
        else:
            self.stats[palace_id]["failed"] += 1
        
        self._save()
        self._check_upgrade(palace_id)
        self._check_downgrade(palace_id)
    
    def record_validation(self, palace_id: int, passed: bool):
        """记录验收结果"""
        if palace_id not in self.stats:
            self.stats[palace_id] = {
                "total": 0,
                "success": 0,
                "failed": 0,
                "validation_passed": 0,
                "current_level": RBACManager.get_default_level(palace_id).value
            }
        
        if passed:
            self.stats[palace_id]["validation_passed"] += 1
        
        self._save()
    
    def _check_upgrade(self, palace_id: int):
        """检查是否可以升级"""
        stats = self.stats.get(palace_id, {})
        current = stats.get("current_level", RBACManager.get_default_level(palace_id).value)
        
        # 升级条件
        upgrade_rules = [
            # (当前等级, 目标等级, 成功次数, 验收通过率)
            (PermissionLevel.L1_APPROVAL.value, PermissionLevel.L2_NOTIFY.value, 10, 0.9),
            (PermissionLevel.L2_NOTIFY.value, PermissionLevel.L3_AUTO.value, 50, 0.95),
            (PermissionLevel.L3_AUTO.value, PermissionLevel.L4_AUTONOMOUS.value, 100, 0.98),
        ]
        
        for current_lv, target_lv, success_count, pass_rate in upgrade_rules:
            if current == current_lv:
                total = stats.get("success", 0)
                validations = stats.get("validation_passed", 0)
                rate = validations / total if total > 0 else 0
                
                if total >= success_count and rate >= pass_rate:
                    stats["current_level"] = target_lv
                    self._save()
                    break
    
    def _check_downgrade(self, palace_id: int):
        """检查是否需要降级"""
        stats = self.stats.get(palace_id, {})
        current = stats.get("current_level", RBACManager.get_default_level(palace_id).value)
        
        # 降级条件：连续失败
        failed = stats.get("failed", 0)
        total = stats.get("total", 0)
        
        if total > 0 and failed / total > 0.2:  # 失败率超过20%
            if current > RBACManager.get_default_level(palace_id).value:
                stats["current_level"] = current - 1
                self._save()
    
    def get_current_level(self, palace_id: int) -> PermissionLevel:
        """获取当前权限等级"""
        if palace_id in self.stats:
            return PermissionLevel(self.stats[palace_id].get("current_level", 
                                   RBACManager.get_default_level(palace_id).value))
        return RBACManager.get_default_level(palace_id)


# ==================== 便捷函数 ====================

def check_permission(palace_id: int, operation: OperationType) -> tuple[bool, str]:
    """检查权限（便捷函数）"""
    pm = PermissionManager()
    current_level = pm.get_current_level(palace_id)
    return PermissionChecker.can_execute(palace_id, operation, current_level)


def require_approval(operation: OperationType) -> bool:
    """判断是否需要审批"""
    level = PermissionChecker.get_required_level(operation)
    return level in [PermissionLevel.L0_FORBIDDEN, PermissionLevel.L1_APPROVAL]


def log_audit(palace: int, action: str, task: str, result: str, 
              duration_ms: int = 0, instruction: str = "") -> AuditLog:
    """记录审计日志（便捷函数）"""
    am = AuditManager()
    return am.log(
        session_id="current_session",  # 实际使用时传入
        palace=palace,
        action=action,
        task_type=task,
        result=result,
        duration_ms=duration_ms,
        user_instruction=instruction
    )


# ==================== 示例用法 ====================

if __name__ == "__main__":
    # 检查权限
    can_exec, reason = check_permission(1, OperationType.DATA_COLLECTION)
    print(f"1宫执行数据采集: {can_exec}, {reason}")
    
    can_exec, reason = check_permission(1, OperationType.DELETE_PALACE)
    print(f"1宫删除宫位: {can_exec}, {reason}")
    
    # 创建审批请求
    am = ApprovalManager()
    request = am.create_request(3, OperationType.PUBLISH_CONTENT)
    print(f"审批请求创建: {request.request_id}")
    
    # 记录审计
    log_audit(5, "dispatch", "video_transcribe", "success", 1234, "下载视频")
    
    # 权限管理
    pm = PermissionManager()
    for i in range(100):
        pm.record_execution(1, success=True)
        pm.record_validation(1, passed=True)
    
    print(f"1宫权限等级: {pm.get_current_level(1).name}")