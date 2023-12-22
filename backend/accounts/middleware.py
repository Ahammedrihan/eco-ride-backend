

class AmountMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.amount_details = None
        response = self.get_response(request)
        return response
        


        