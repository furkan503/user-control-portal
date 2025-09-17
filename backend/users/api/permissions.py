# from rest_framework import permissions

# # class IsAdminUserOrReadOnly(permissions.IsAdminUser):
# #      def has_permission(self,request,view):
# #          is_admin = super().has_permission(request, view)
# #          return request.method in permissions.SAFE_METHODS or is_admin


# class CanEditTodos(permissions.BasePermission):
#     """
#     Custom permission to only allow users with 'edit_todo' permission to edit todos.
#     """
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user.has_perm('app_name.edit_todo')