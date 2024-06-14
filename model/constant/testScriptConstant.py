STATUS_VALIDATE_SCRIPT = """
pm.test('Status code is {{status_code}}', function () {
    pm.response.to.have.status({{status_code}});
});"""

RESPONSE_BODY_TYPE_CHECK_SCRIPT ="""
pm.test('Response body should not be null or empty', function () {
    let responseBody = pm.response.text();
    pm.expect(responseBody).to.not.be.null;
    pm.expect(responseBody.trim()).to.not.be.empty;
});"""


BEARER_TOKEN_SET_SCRIPT = """
pm.request.headers.add({
    key: 'Authorization', value: 'Bearer {{access_token}}'
});"""
