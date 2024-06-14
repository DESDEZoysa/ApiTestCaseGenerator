PARAMETER_STRING_VALUE = {
    "200":[
            "abcd",
            "abc@123def"
        ],
    "400":[
            None,
            "",
        ]        
}

PARAMETER_EMAIL_VALUE = {
    "200":[
            "abc@gmail.com",
            "abc@efg.ghi",
            "abc@e",
        ],
    "400":[
            None,
            "",
            "abcghi",
            "abc@"
        ]   
}

PARAMETER_MOBILE_VALUE = {
    "200":[
            "1234567891",
            "%2B1234567891",
            "%2B1234567891234"
        ],
    "400":[
            None,
            "",
            "123456789",
            "%2B123456789",
            "%2B12345678912345",
            
        ]   
}

PARAMETER_DATE_TIME_VALUE = {
    "200":[
            "2027/04/23 09:34:23",            
            "2067/04/23"
        ],
    "400":[
            None,
            "" ,
            "2067-04-23 09:34:34",
        ]   
}

PARAMETER_INTEGER_VALUE = {
    "200":[
            "0",
            "123",
            "-12345"
        ],
    "400":[
            None,
            "",
            "123456876543345676543345676534566543"            
        ]   
}

PARAMETER_BOOLEAN_VALUE = {
    "200":[
            "true",
            "false"
        ],
    "400":[
            None,
            ""                       
        ]   
}

AUTTHENTICATION_DETAIL = {
    "authUrl":"http://localhost:8091/auth/login",
    "userName":"eranga123",
    "password":"eranga123",
    "userNameKey":"userName",
    "passwordKey":"password",
    "requestBody":{
                    "userName": "eranga123",
                    "password": "eranga123"
                    },
    "tokenPath":"data.accessToken"
}  

ACCESS_TOKEN = ""

