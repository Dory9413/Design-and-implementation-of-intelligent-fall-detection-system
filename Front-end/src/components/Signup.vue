<template>
    <div>
        <div class="body w-100 d-none d-lg-flex flex-row align-items-center justify-content-center">
            <div class="box w-50 d-flex flex-row justify-content-between">
                <div class="d-flex flex-column" style="width: 48%">
                    <div class="title">نام</div>
                    <input class="user-input" v-model="firstName">
                    <p style="color: red">{{ fields_errors.firstname }}</p>
                    <div class="title">شماره موبایل</div>
                    <input class="user-input" v-model="phoneNumber">
                    <p style="color: red">{{ fields_errors.phone }}</p>
                    <div class="title">تاریخ تولد</div>
                    <input class="user-input" v-model="birthDate">
                    <p style="color: red">{{ fields_errors.birthday }}</p>
                    <div class="title">نام کاربری</div>
                    <input class="user-input" v-model="username">
                    <p style="color: red">{{ fields_errors.username }}</p>
                    <div class="title">رمز عبور</div>
                    <input class="user-input" type="password" v-model="password">
                    <p style="color: red">{{ fields_errors.password }}</p>
                    <div class="w-100 d-flex flex-row">
                        <router-link to="/login" class="option d-flex justify-content-center align-items-center">ورود
                        </router-link>
                    </div>
                </div>
                <div class="d-flex flex-column" style="width: 48%">
                    <div class="title">نام خانوادگی</div>
                    <input class="user-input" v-model="lastName">
                    <p style="color: red">{{ fields_errors.lastname }}</p>
                    <div class="title">ایمیل</div>
                    <input class="user-input" v-model="email">
                    <p style="color: red">{{ fields_errors.email }}</p>
                    <div class="title">جنسیت</div>
                    <input class="user-input" v-model="gender">
                    <p style="color: red">{{ fields_errors.gender }}</p>
                    <div class="title">کد ساعت</div>
                    <input class="user-input" v-model="watchId">
                    <p style="color: red">{{ fields_errors.watch_code }}</p>
                    <div class="title">تکرار رمز عبور</div>
                    <input class="user-input" type="password" v-model="passwordConfirm">
                    <p style="color: red">{{ fields_errors.password_confirm }}</p>

                    <div class="w-100 d-flex flex-row-reverse">
                        <p v-on:click="signUp"
                           class="option d-flex justify-content-center align-items-center buttonstyle">ثبت نام</p>
                    </div>
                    <p style="white-space: pre; color: red;">{{ response_error }}</p>
                </div>
            </div>
            <div @click="$router.push('/')" class="w-50 d-flex flex-column justify-content-center align-items-center">
                <i class="mdi mdi-watch iconstyle"></i>
                <div class="big-title">ثبت نام</div>
            </div>
        </div>
        <mobile-signup v-if="ismobile"></mobile-signup>
    </div>
</template>

<script>
import axios from 'axios'
import MobileSignup from "@/components/Mobile/MobileSignup";

export default {
    name: "Signup",
    components: {MobileSignup},
    data() {
        return {
            firstName: '',
            lastName: '',
            phoneNumber: '',
            email: '',
            birthDate: '',
            gender: '',
            username: '',
            watchId: '',
            password: '',
            passwordConfirm: '',
            response_error: '',
            ismobile: false,
            fields_errors: {
                firstname: '',
                lastname: '',
                phone: '',
                birthday: '',
                username: '',
                password: '',
                email: '',
                gender: '',
                watch_code: '',
                password_confirm: ''
            }
        }
    }, methods: {
        onResize(){
            if (window.innerWidth > 1000){
                this.ismobile = false;
            }
            else
                this.ismobile = true;
        },
        async signUp() {
            await axios.post(this.$baseUrl + "/users/app/signup/", {
                username: this.username,
                password: this.password,
                password_confirm: this.passwordConfirm,
                phone: this.phoneNumber,
                email: this.email,
                firstname: this.firstName,
                lastname: this.lastName,
                gender: this.gender,
                watch_code: this.watchId,
                birthday: this.birthDate
            })
                .then((response) => {
                    localStorage.access_token = response.data.jwt_access_token
                    localStorage.refresh_token = response.data.jwt_refresh_token
                    this.response_error = ''
                    for (var key in this.fields_errors) {
                        this.fields_errors[key] = ''
                    }
                    this.$router.push({'name': 'Panel'})
                })
                .catch((error) => {
                    if (error.response) {
                        if (error.response.status == 400) {
                            this.fields_errors = error.response.data
                            this.response_error = ''
                        }
                        if (error.response.status == 409) {
                            this.response_error = 'کاربری با این اطلاعات قبلا ثبت شده است'
                            for (var key in this.fields_errors) {
                                this.fields_errors[key] = ''
                            }
                        }
                    } else {
                        console.warn(error)
                        this.response_error = 'ارتباط با سرور با مشکل مواجه شده است'
                        for (var key in this.fields_errors) {
                            this.fields_errors[key] = ''
                        }
                    }
                })

        }
    },
    created(){
        window.addEventListener('resize', this.onResize)
        this.onResize()
    },

    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    }
}
</script>

<style scoped>
.mdi-watch {
    font-size: 100px;
}

.body {
    height: 100vh;
    padding: 48px;
}

.user-input {
    margin-bottom: 24px;
}

.iconstyle:hover {
    color: #111E6c;
}

.buttonstyle {
    color: white;
    background-color: #111E6c;
}

.buttonstyle:hover {
    background-color: #23318d;
}

</style>
