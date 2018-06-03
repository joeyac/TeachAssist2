# teach assist system
### 一些信息
管理账号：

    username: root
    
    password: password@root
    
封装了一些有用的函数和装饰器，对于views.py的编写请参考account.views

account.decorators中实现了一些装饰器，使用方法如下：
    
    from account.decorators import secretary_required

    class XXXAPI(APIView):
    
        @secretary_required
        def post(self, request):
            """
            说明该post方法要求教学秘书登录才能访问
            """
            pass