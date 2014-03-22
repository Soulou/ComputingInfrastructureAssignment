import saga

class Factory:
    _args = None

    @classmethod
    def setup(cls, args):
        Factory._args = args

    @classmethod
    def new(cls):
        ctx = None
        if Factory._args.certificate != None:
            ctx = saga.Context("X509")
            ctx.user_proxy = Factory._args.certificate
        else:
            ctx = saga.Context("ssh")
            if Factory._args.identity != None:
                ctx.user_key = Factory._args.identity

        ctx.user_id  = Factory._args.user
        session = saga.Session()
        session.add_context(ctx)

        return session

