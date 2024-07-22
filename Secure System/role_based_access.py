class RoleBasedAccessControl:
    def __init__(self):
        self.roles = {
            "admin": {"create", "read", "update", "delete"},
            "user": {"create", "read", "update"}
        }

    def has_permission(self, role, action):
        return action in self.roles.get(role, set())
