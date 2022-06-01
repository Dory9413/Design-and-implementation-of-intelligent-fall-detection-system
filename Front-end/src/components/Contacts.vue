<template>
    <div>
        <div class="body w-100 d-none d-lg-flex flex-row align-items-center justify-content-center">
            <div class="box w-50 d-flex flex-row justify-content-between">
                <div class="d-flex flex-column" style="width: 48%">
                    <div class="title">نام مخاطب اول</div>
                    <input class="user-input" v-model="contactOne">
                    <p style="color: red">{{ fields_errors.contact_1 }}</p>
                    <div class="title">نام مخاطب دوم</div>
                    <input class="user-input" v-model="contactTwo">
                    <p style="color: red">{{ fields_errors.contact_2 }}</p>
                    <div class="title">نام مخاطب سوم</div>
                    <input class="user-input" v-model="contactThree">
                    <p style="color: red">{{ fields_errors.contact_3 }}</p>
                    <div class="title">نام مخاطب چهارم</div>
                    <input class="user-input" v-model="contactFour">
                    <p style="color: red">{{ fields_errors.contact_4 }}</p>
                    <div class="title">نام مخاطب پنجم</div>
                    <input class="user-input" v-model="contactFive">
                    <p style="color: red">{{ fields_errors.contact_5 }}</p>
                </div>
                <div class="d-flex flex-column" style="width: 48%">
                    <div class="title">شماره مخاطب اول</div>
                    <input class="user-input" v-model="phoneOne">
                    <p style="color: red">{{ fields_errors.phone_1 }}</p>
                    <div class="title">شماره مخاطب دوم</div>
                    <input class="user-input" v-model="phoneTwo">
                    <p style="color: red">{{ fields_errors.phone_2 }}</p>
                    <div class="title">شماره مخاطب سوم</div>
                    <input class="user-input" v-model="phoneThree">
                    <p style="color: red">{{ fields_errors.phone_3 }}</p>
                    <div class="title">شماره مخاطب چهارم</div>
                    <input class="user-input" v-model="phoneFour">
                    <p style="color: red">{{ fields_errors.phone_4 }}</p>
                    <div class="title">شماره مخاطب پنجم</div>
                    <input class="user-input" v-model="phoneFive">
                    <p style="color: red">{{ fields_errors.phone_5 }}</p>
                    <div class="w-100 d-flex flex-row-reverse">
                        <p v-on:click="updateContacts" class="option d-flex justify-content-center align-items-center"
                           style="background-color: lightslategray; color: white;">تایید</p>
                    </div>
                    <p style="color: red">{{ error_message }}</p>
                    <p style="color: green">{{ message }}</p>
                </div>
            </div>
            <div class="w-50 d-flex flex-column justify-content-center align-items-center">
                <i class="mdi mdi-watch"></i>
                <div class="big-title">تکمیل اطلاعات</div>
            </div>
        </div>
        <mobile-contacts></mobile-contacts>
    </div>
</template>

<script>
import axios from 'axios'
import MobileContacts from "@/components/Mobile/MobileContacts";

export default {
    name: "Contacts",
    components: {MobileContacts},
    data() {
        return {
            contactOne: '',
            phoneOne: '',
            contactTwo: '',
            phoneTwo: '',
            contactThree: '',
            phoneThree: '',
            contactFour: '',
            phoneFour: '',
            contactFive: '',
            phoneFive: '',
            error_message: '',
            message: '',
            fields_errors: {
                contact_1: '',
                contact_2: '',
                contact_3: '',
                contact_4: '',
                contact_5: '',
                phone_1: '',
                phone_2: '',
                phone_3: '',
                phone_4: '',
                phone_5: ''
            }
        }
    }, created() {
        axios.get(this.$baseUrl + '/users/app/view-contacts/', {
            headers: {
                Authorization: 'Bearer ' + localStorage.access_token
            }
        })
            .then((response) => {
                for (var key in this.fields_errors) {
                    this.fields_errors[key] = ''
                }
                this.error_message = ''
                this.contactOne = response.data.contact_1
                this.contactTwo = response.data.contact_2
                this.contactThree = response.data.contact_3
                this.contactFour = response.data.contact_4
                this.contactFive = response.data.contact_5
                this.phoneOne = response.data.phone_1
                this.phoneTwo = response.data.phone_2
                this.phoneThree = response.data.phone_3
                this.phoneFour = response.data.phone_4
                this.phoneFive = response.data.phone_5
            })
            .catch((error) => {
                if (error.response) {
                    if (error.response.status == 401) {
                        for (var key in this.fields_errors) {
                            this.fields_errors[key] = ''
                        }
                        this.error_message = 'برای دسترسی به این بخش باید ابتدا وارد شوید'
                    }
                } else {
                    for (var key in this.fields_errors) {
                        this.fields_errors[key] = ''
                    }
                    this.error_message = 'ارتباط با سرور قطع است'
                }
            })
    }, methods: {
        async updateContacts() {
            axios.post(this.$baseUrl + '/users/app/update-contacts/', {
                contact_1: this.contactOne,
                contact_2: this.contactTwo,
                contact_3: this.contactThree,
                contact_4: this.contactFour,
                contact_5: this.contactFive,
                phone_1: this.phoneOne,
                phone_2: this.phoneTwo,
                phone_3: this.phoneThree,
                phone_4: this.phoneFour,
                phone_5: this.phoneFive
            }, {
                headers: {
                    Authorization: 'Bearer ' + localStorage.access_token
                }
            })
                .then((response) => {
                    this.message = "مخاطبان کاربر به روز رسانی شدند"
                    this.error_message = ''
                    for (var key in this.fields_errors) {
                        this.fields_errors[key] = ''
                    }
                })
                .catch((error) => {
                    if (error.response) {
                        if (error.response.status == 401) {
                            this.message = ''
                            for (var key in this.fields_errors) {
                                this.fields_errors[key] = ''
                            }
                            this.error_message = 'برای استفاده از این بخش باید ابتدا وارد شوید'
                        }
                        if (error.response.status == 400) {
                            console.warn(error.response.data)
                            this.fields_errors = error.response.data
                            this.error_message = ''
                            this.message = ''
                        }
                    } else {
                        for (var key in this.fields_errors) {
                            this.fields_errors[key] = ''
                        }
                        this.error_message = 'ارتباط با سرور با مشکل مواجه شده است'
                    }
                })
        }
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
</style>