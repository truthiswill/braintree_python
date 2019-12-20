import cgi

from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult
from braintree.exceptions.unexpected_error import UnexpectedError


class ApplePayGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def register_domain(self, domain):
        response = self.config.http().post(self.config.base_merchant_path() + "/processing/apple_pay/validate_domains", {'url': domain})

        if "response" in response and response["response"]["success"]:
            return SuccessfulResult()
        elif response["api_error_response"]:
            return ErrorResult(self.gateway, response["api_error_response"])

    def unregister_domain(self, domain):
        self.config.http().delete(self.config.base_merchant_path() + "/processing/apple_pay/unregister_domain?url=" + cgi.escape(domain))
        return SuccessfulResult()

        return ErrorResult(self.gateway, 'An unexpected error occurred.')

    def registered_domains(self):
        response = self.config.http().get(self.config.base_merchant_path() + "/processing/apple_pay/registered_domains")

        if "response" in response:
            response = response["response"]

        return response["domains"]
