from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from account_module.models import User, UserOTP


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            phone_number="09123456789",
            email="test@example.com",
            password="TestPassword123",
            is_verified=False
        )

    def test_user_registration_success(self):
        response = self.client.post(reverse("account_module:user-register"), {
            "phone_number": "09111111111",
            "email": "newuser@example.com",
            "password": "SecurePass123",
            "confirm_password": "SecurePass123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(phone_number="09111111111").exists())

    def test_user_registration_duplicate_phone(self):
        response = self.client.post(reverse("account_module:user-register"), {
            "phone_number": "09123456789",
            "email": "duplicate@example.com",
            "password": "SecurePass123",
            "confirm_password": "SecurePass123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "این شماره تلفن قبلا استفاده شده است")

    def test_otp_generation_on_registration(self):
        self.client.post(reverse("account_module:user-register"), {
            "phone_number": "09112223344",
            "email": "otpuser@example.com",
            "password": "SecurePass123",
            "confirm_password": "SecurePass123"
        })
        user = User.objects.get(phone_number="09112223344")
        self.assertTrue(UserOTP.objects.filter(user=user).exists())

    def test_login_success(self):
        response = self.client.post(reverse("account_module:user-login"), {
            "phone_number": "09123456789",
            "password": "TestPassword123"
        })
        self.assertEqual(response.status_code, 302) #because is_verified field is false

    def test_login_unverified_user_redirects_to_otp(self):
        response = self.client.post(reverse("account_module:user-login"), {
            "phone_number": "09123456789",
            "password": "TestPassword123"
        })
        self.assertRedirects(response, reverse("account_module:user-otp-code") + "?flow=signup")

    # not complete
    def test_otp_verification_success(self):
        # Store OTP in database and cache
        otp_instance = UserOTP.objects.create(user=self.user, otp="123456")
        cache.set(f"otp:{self.user.phone_number}", "123456", timeout=900)  # Store OTP in cache
        cache.set(f"phone_number:test_session", self.user.phone_number, timeout=900)  # Store phone number in cache

        # Retrieve OTP from Redis (Cache)
        redis_otp = cache.get(f"otp:{self.user.phone_number}")
        # print("Redis OTP:", redis_otp)  # Should print "123456"
        
        # Simulate user submitting OTP fields in the form
        submitted_otp = "".join(["1", "2", "3", "4", "5", "6"])  # Should reconstruct "123456"
        # print("Submitted OTP:", submitted_otp)

        # Ensure they match
        self.assertEqual(redis_otp, submitted_otp, "Cached OTP does not match submitted OTP")

        # Make POST request with the OTP fields
        response = self.client.post(
            reverse("account_module:user-otp-code") + "?flow=signup",
            {
                "input1": "1",
                "input2": "2",
                "input3": "3",
                "input4": "4",
                "input5": "5",
                "input6": "6",
            }
        )
        # Debugging output
        # print("Response Status Code:", response.status_code)
        # print("Response Content:", response.content.decode())
        # print("Redirect Location:", response.headers.get("Location"))

    def test_forget_password_flow(self):
        response = self.client.post(reverse("account_module:user-forget-password"), {
            "phone_number": "09123456789"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("account_module:user-otp-code") + "?flow=forget_password")

    # def test_unregistered_phone_number_forget_password_flow(self):
    #     response = self.client.post(reverse("account_module:user-forget-password"), {
    #         "phone_number": "08123456789"
    #     })
    #     self.assertEqual(response.status_code, 400)
    #     # self.assertRedirects(response, reverse("account_module:user-forget-password"))

    def test_change_password_success(self):
        session=self.client.session
        session_key=session.session_key
        cache.set(f"verified_user:{session_key}", self.user.phone_number, timeout=900)
        # cache.set(f"verified_user:test_session", self.user.phone_number, timeout=900)
        response = self.client.post(reverse("account_module:user-change-password"), {
            "password": "NewPassword123",
            "confirm_password": "NewPassword123"
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPassword123"))

    def test_url_resolves(self):
        self.assertEqual(reverse("account_module:user-register"), "/account/register/")
        self.assertEqual(reverse("account_module:user-login"), "/account/login/")
        self.assertEqual(reverse("account_module:user-forget-password"), "/account/forget-password/")
        self.assertEqual(reverse("account_module:user-otp-code"), "/account/otp-code/")
        self.assertEqual(reverse("account_module:user-change-password"), "/account/change-password/")























    # def test_otp_verification_success(self):
    #     otp_instance = UserOTP.objects.create(user=self.user, otp="123456")

    #     # print(otp_instance.user)
    #     # print(otp_instance.user.is_verified)
    #     # print(otp_instance.user.phone_number)
    #     cache.set(f"otp:{self.user.phone_number}", "123456", timeout=900) # 123456
    #     cache.set(f"phone_number:test_session", self.user.phone_number, timeout=900) # 09123456789
        
    #     response = self.client.post((reverse("account_module:user-otp-code") + "?flow=signup"), {
    #         "input1": "1", "input2": "2", "input3": "3", "input4": "4", "input5": "5", "input6": "6"
    #     },follow=True)
    #     self.user.refresh_from_db()
    #     self.assertRedirects(response, reverse("account_module:user-login"))
    #     # print("user verification=",self.user.is_verified)
    #     print('response= ',response)
    #     self.assertEqual(response.status_code, 302)
    #     # self.assertTrue(self.user.is_verified)

    # def test_otp_verification_success(self):
    #     otp_instance = UserOTP.objects.create(user=self.user, otp="123456")
    #     cache.set(f"otp:{self.user.phone_number}", "123456", timeout=900)  # Store OTP in cache
    #     cache.set(f"phone_number:test_session", self.user.phone_number, timeout=900)  # Store phone number in cache
    #     # print('otp cached from redis== ',cache.get(f"otp:{self.user.phone_number}"))
    #     redis_otp=cache.get(f"otp:{self.user.phone_number}")
    #     print("redis checking is == ",redis_otp == "123456") # it returns True

    #     response = self.client.post(
    #         reverse("account_module:user-otp-code") + "?flow=signup",
    #         {"input1": "1", "input2": "2", "input3": "3", "input4": "4", "input5": "5", "input6": "6"}
    #     )
    #     # print(response.content.decode())
    #     # self.user.refresh_from_db()
    #     # self.assertRedirects(response, reverse("account_module:user-login"))  # Expecting 302
