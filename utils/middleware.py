

class UrlPathRecodeMiddleware(object):
    '''用户访问URL地址中间件 在session中保存用户访问的地址 并在登陆后返回 注意需要在settings中注册'''
    EXCLUDE_URLS = ["/user/login", "/user/register", "/user/register_handle", "user/logout"]

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path not in self.EXCLUDE_URLS and not request.is_ajax and requset.method == "GET":
            # 保存这个地址
            request.session["url_path"] = request.path
