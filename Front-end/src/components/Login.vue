<template>
    <div>
        <div class="body w-100 d-none d-lg-flex flex-row align-items-center justify-content-center">
            <div class="w-50 d-flex justify-content-center align-items-center">
                <div class="box w-50 d-flex flex-column">
                    <div class="title">نام کاربری</div>
                    <input class="user-input" v-model="username">
                    <p style="color: red;">{{ fields_errors.username }}</p>
                    <div class="title">رمز عبور</div>
                    <input class="user-input" type="password" v-model="password">
                    <p style="color: red;">{{ fields_errors.password }}</p>
                    <p style="white-space: pre; color: red;">{{ response_code }}</p>
                    <div class="w-100 d-flex flex-row justify-content-between align-items-center">
                        <p v-on:click="login" class="option d-flex justify-content-center align-items-center">ورود</p>
                        <router-link to="/signup" class="option d-flex justify-content-center align-items-center">ثبت
                            نام
                        </router-link>
                    </div>
                </div>
            </div>
            <div @click="$router.push('/')" class="w-50 d-flex flex-column justify-content-center align-items-center">
                <i class="mdi mdi-watch iconstyle"></i>
                <div class="big-title">ورود</div>
            </div>
        </div>
        <mobile-login v-if="ismobile"></mobile-login>
    </div>
</template>

<script>
import axios from 'axios'
import MobileLogin from "@/components/Mobile/MobileLogin";

export default {
    name: "Login",
    components: {MobileLogin},
    data() {
        return {
            username: '',
            password: '',
            response_code: '',
            ismobile: false,
            fields_errors: {
                username: '',
                password: ''
            }
        }
    },
    methods: {
        onResize(){
            if (window.innerWidth > 1000){
                this.ismobile = false;
            }
            else
                this.ismobile = true;
        },
        async login() {
            console.log('HERRRE')
            let result = await axios.post(this.$baseUrl + "/users/app/login/", {
                username: this.username,
                password: this.password
            }).then((response) => {
                localStorage.access_token = response.data.jwt_access_token
                localStorage.refresh_token = response.data.jwt_refresh_token
                for (var key in this.fields_errors) {
                    this.fields_errors[key] = ''
                }
                this.response_code = ''
                console.log('HEREE2')
                this.$router.push({'name': 'Panel'})
                console.log('HEREE3')
            })
                .catch((error) => {
                    if (error.response) {
                        if (error.response.status == 400) {
                            console.warn(error.response.data)
                            this.fields_errors = error.response.data
                        }
                        if (error.response.status == 403) {
                            for (var key in this.fields_errors) {
                                this.fields_errors[key] = ''
                            }
                            this.response_code = error.response.data
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

.iconstyle:hover {
    color: #111E6c;
}

.user-input {
    margin-bottom: 24px;
}
</style>