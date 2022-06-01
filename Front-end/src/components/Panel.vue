<template>
    <div>
        <div class="body d-none d-lg-flex flex-row">
            <div class="nav-bar d-flex flex-column justify-content-between">
                <div class="d-flex w-100 flex-column align-items-center">
                    <router-link to="/">
                        <i class="mdi mdi-watch iconstyle"></i>
                    </router-link>
                    <div class="big-title-1">سامانه‌ی هوشمند تشخیص افتادن</div>
                    <div class="option-1 w-100 d-flex align-items-center" @click="selected = 'personalInfo'"
                         :style="(selected === 'personalInfo') ? {backgroundColor: '#eeeeee'} : ''">اطلاعات شخصی
                    </div>
                    <div class="option-1 w-100 d-flex align-items-center" @click="selected = 'contacts'"
                         :style="(selected === 'contacts') ? {backgroundColor: '#eeeeee'} : ''">مخاطبان
                    </div>
                    <div class="option-1 w-100 d-flex align-items-center" @click="selected = 'locationInfo'"
                         :style="(selected === 'locationInfo') ? {backgroundColor: '#eeeeee'} : ''">اطلاعات مکانی و
                        ضربان قلب
                    </div>
                </div>
                <p v-on:click="logout" class="exit-btn">خروج</p>
            </div>
            <div class="info-box w-100 d-flex justify-content-center align-items-center">
                <div v-if="selected === 'personalInfo'" class="w-75 d-flex flex-row justify-content-between">
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
                            <div v-on:click="updateUser"
                                 class="option d-flex justify-content-center align-items-center buttonstyle">تایید
                            </div>
                        </div>
                        <p style="color: red">{{ general_error }}</p>
                        <p style="color: green">{{ general_message }}</p>
                    </div>
                </div>
                <div v-else-if="selected === 'locationInfo'" class="w-75 d-flex flex-column justify-content-between">
                    <div class="W-100 d-flex flex-column">
                        <div class="big-title">مشخصات مکانی</div>
                        <div class="user-input box-1 w-100">
                            <iframe id="map_iframe" width=100% height=100% frameborder="0" style="border:0" hidden
                                :src='map_url' allowfullscreen>
                            </iframe>
                        </div>
                    </div>
                    <div class="W-100 d-flex flex-column">
                        <div class="big-title">ضربان قلب</div>
                        <div class="user-input box-2 w-100 d-flex flex-row">
                            <iframe id="first_diagram_iframe" hidden style="border: 1px solid #cccccc; Border-radius: 10px;
                        Overflow: hidden; width:50%; height: 100%;"
                                    src='https://thingspeak.com/channels/1726304/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&yaxismax=150&yaxismin=0'>
                            </iframe>
                            <iframe id="second_diagram_iframe" hidden style="border: 1px solid #cccccc; Border-radius: 10px;
                        Overflow: hidden; width:50%; height: 100%;"
                                    src='https://thingspeak.com/channels/1726304/widgets/457246'>
                            </iframe>
                        </div>
                    </div>
                </div>
                <div v-else class="w-75 d-flex flex-row justify-content-between">
                    <div class="d-flex flex-column" style="width: 48%">
                        <div class="title">نام مخاطب اول</div>
                        <input class="user-input" v-model="contactOne">
                        <p style="color: red">{{ contacts_fields_errors.contact_1 }}</p>
                        <div class="title">نام مخاطب دوم</div>
                        <input class="user-input" v-model="contactTwo">
                        <p style="color: red">{{ contacts_fields_errors.contact_2 }}</p>
                        <div class="title">نام مخاطب سوم</div>
                        <input class="user-input" v-model="contactThree">
                        <p style="color: red">{{ contacts_fields_errors.contact_3 }}</p>
                        <div class="title">نام مخاطب چهارم</div>
                        <input class="user-input" v-model="contactFour">
                        <p style="color: red">{{ contacts_fields_errors.contact_4 }}</p>
                        <div class="title">نام مخاطب پنجم</div>
                        <input class="user-input" v-model="contactFive">
                        <p style="color: red">{{ contacts_fields_errors.contact_5 }}</p>
                    </div>
                    <div class="d-flex flex-column" style="width: 48%">
                        <div class="title">شماره مخاطب اول</div>
                        <input class="user-input" v-model="phoneOne">
                        <p style="color: red">{{ contacts_fields_errors.phone_1 }}</p>
                        <div class="title">شماره مخاطب دوم</div>
                        <input class="user-input" v-model="phoneTwo">
                        <p style="color: red">{{ contacts_fields_errors.phone_2 }}</p>
                        <div class="title">شماره مخاطب سوم</div>
                        <input class="user-input" v-model="phoneThree">
                        <p style="color: red">{{ contacts_fields_errors.phone_3 }}</p>
                        <div class="title">شماره مخاطب چهارم</div>
                        <input class="user-input" v-model="phoneFour">
                        <p style="color: red">{{ contacts_fields_errors.phone_4 }}</p>
                        <div class="title">شماره مخاطب پنجم</div>
                        <input class="user-input" v-model="phoneFive">
                        <p style="color: red">{{ contacts_fields_errors.phone_5 }}</p>
                        <div class="w-100 d-flex flex-row-reverse">
                            <p v-on:click="updateContacts"
                               class="option d-flex justify-content-center align-items-center buttonstyle">تایید</p>
                        </div>
                        <p style="color: red">{{ error_message }}</p>
                        <p style="color: green">{{ message }}</p>
                    </div>
                </div>
            </div>
        </div>
        <mobile-panel></mobile-panel>
    </div>
</template>

<script>
import axios from 'axios'
import MobilePanel from "@/components/Mobile/MobilePanel";

export default {
    name: "Panel",
    components: {MobilePanel},
    data() {
        return {
            map_url: "http://www.openstreetmap.org/export/embed.html?bbox=51.45969%2C35.74533%2C51.46369%2C35.74933&marker=35.74733%2C51.46169&layers=ND",
            selected: 'personalInfo',
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
            general_error: '',
            general_message: '',
            fields_errors: {
                firstname: '',
                lastname: '',
                phone: '',
                email: '',
                birthday: '',
                gender: '',
                username: '',
                watch_code: '',
                password: '',
                password_confirm: ''
            },
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
            contacts_fields_errors: {
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
        axios.get(this.$baseUrl + "/users/app/view-user/", {
            headers: {
                Authorization: 'Bearer ' + localStorage.access_token
            }
        })
            .then((response) => {
                this.general_error = ''
                this.firstName = response.data.firstname
                this.lastName = response.data.lastname
                this.phoneNumber = response.data.phone
                this.email = response.data.email
                this.birthDate = response.data.birthday
                this.gender = response.data.gender
                this.username = response.data.username
                this.watchId = response.data.watch_code
            })
            .catch((error) => {
                if (error.response) {
                    if (error.response.status == 401) {
                        this.general_error = 'برای مشاهده ی اطلاعات باید ابتدا وارد شوید'
                    }
                }
            })

        axios.get(this.$baseUrl + '/users/app/view-contacts/', {
            headers: {
                Authorization: 'Bearer ' + localStorage.access_token
            }
        })
            .then((response) => {
                for (var key in this.contacts_fields_errors) {
                    this.contacts_fields_errors[key] = ''
                }
                this.general_error = ''
                this.contacts_fields_errors = ''
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
                        for (var key in this.contacts_fields_errors) {
                            this.contacts_fields_errors[key] = ''
                        }
                        this.error_message = 'برای دسترسی به این بخش باید ابتدا وارد شوید'
                    }
                } else {
                    for (var key in this.contacts_fields_errors) {
                        this.contacts_fields_errors[key] = ''
                    }
                    this.error_message = 'ارتباط با سرور قطع است'
                }
            })
    }, methods: {
        async updateMap() {
            setInterval(() => {
                axios.get(this.$baseUrl + '/users/app/get-gps/', {
                    headers: {
                        Authorization: 'Bearer ' + localStorage.access_token
                    }
                })
                .then((response) => {
                    this.map_url = response.data
                    if (document.getElementById('first_diagram_iframe').hidden == true) {
                        document.getElementById('first_diagram_iframe').hidden = false
                    }
                    if (document.getElementById('second_diagram_iframe').hidden == true) {
                        document.getElementById('second_diagram_iframe').hidden = false
                    }
                    if (document.getElementById('map_iframe').hidden == true) {
                        document.getElementById('map_iframe').hidden = false
                    }
                    document.getElementById('map_iframe').src = this.map_url
                    console.log('map updated with ' + this.map_url + ' url')
                }).
                catch(error => {
                    if (!error.response) {
                        console.log('Error: Network Error')
                    } else if (error.response.status == 401)  {
                        document.getElementById('map_iframe').hidden = true
                    } else {
                        console.log(error.response)
                    }
                })
            }, 20000)
        },
        async updateUser() {
            axios.post(this.$baseUrl + '/users/app/update-user/',
                {
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
                },
                {
                    headers: {
                        Authorization: 'Bearer ' + localStorage.access_token
                    }
                })
                .then((response) => {
                    this.general_error = ''
                    this.general_message = 'پروفایل کاربر به روز رسانی شد'
                })
                .catch((error) => {
                    if (error.response) {
                        if (error.response.status == 401) {
                            for (var key in this.fields_errors) {
                                this.fields_errors[key] = ''
                            }
                            this.general_error = 'برای دسترسی به این بخش، باید ابتدا وارد شوید'
                        } else if (error.response.status == 409) {
                            for (var key in this.fields_errors) {
                                this.fields_errors[key] = ''
                            }
                            this.general_error = error.response.data.message
                        } else if (error.response.status == 400) {
                            this.fields_errors = error.response.data
                        }
                    } else {
                        for (var key in this.fields_errors) {
                            this.fields_errors[key] = ''
                        }
                        this.general_error = 'عدم ارتباط با سرور'
                    }
                })
        },
        logout() {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            this.$router.push({'name': 'Main Menu'})
        },
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
                    for (var key in this.contacts_fields_errors) {
                        this.contacts_fields_errors[key] = ''
                    }
                })
                .catch((error) => {
                    if (error.response) {
                        if (error.response.status == 401) {
                            this.message = ''
                            for (var key in this.contacts_fields_errors) {
                                this.contacts_fields_errors[key] = ''
                            }
                            this.error_message = 'برای استفاده از این بخش باید ابتدا وارد شوید'
                        }
                        if (error.response.status == 400) {
                            console.warn(error.response.data)
                            this.contacts_fields_errors = error.response.data
                            this.error_message = ''
                            this.message = ''
                        }
                    } else {
                        for (var key in this.contacts_fields_errors) {
                            this.contacts_fields_errors[key] = ''
                        }
                        this.error_message = 'ارتباط با سرور با مشکل مواجه شده است'
                    }
                })
        }
    },
    mounted () {
        this.updateMap()
    }
}
</script>

<style scoped>
.mdi-watch {
    font-size: 100px;
}

.body {
    height: 100vh;
    width: 100vw;
    overflow: hidden;
}

.nav-bar {
    height: 100%;
    min-width: 330px;
    border-radius: 20px 0 0 20px;
    background-color: white;
    box-shadow: 0 1px 7px 8px rgba(0, 0, 0, 0.06);
    padding: 36px 0 36px 24px;
}

.big-title-1 {
    font-size: 22px;
    margin-bottom: 48px;
    text-align: center;
}

.option-1 {
    cursor: pointer;
    border-radius: 20px 0 0 20px;
    font-size: 20px;
    padding: 20px 24px;
    margin-bottom: 12px;
}

.option-1:hover {
    box-shadow: inset 0 0 1px 1px #eeeeee;
}

.user-input {
    margin-bottom: 24px;
}

.big-title {
    margin-bottom: 24px;
}

.box-1 {
    height: 350px;
}

.buttonstyle {
    color: white;
    background-color: #111E6c;
}

.buttonstyle:hover {
    background-color: #23318d;
}

.box-2 {
    height: 250px;
}

.iconstyle:hover {
    color: #111E6c;
}

.exit-btn {
    font-size: 22px;
    width: fit-content;
    background-color: whitesmoke;
    color: firebrick;
    padding: 20px 24px 20px 34px;
    border-radius: 20px 0 0 20px;
    cursor: pointer;
}
</style>