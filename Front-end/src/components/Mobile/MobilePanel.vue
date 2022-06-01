<template>
    <div class="w-100 d-flex d-lg-none flex-column">
        <div class="header w-100 d-flex flex-row justify-content-between align-items-center">
            <i class="mdi mdi-menu" @click="showMenu = true"></i>
            <div class="d-flex flex-row align-items-center">
                <i class="mdi mdi-watch"></i>
                <div>سامانه‌ی هوشمند تشخیص افتادن</div>
            </div>
        </div>
        <div v-if="showMenu">
            <div class="nav-bar d-flex flex-column justify-content-between">
                <div class="d-flex w-100 flex-column align-items-center">
                    <div class="option-1 w-100 d-flex align-items-center" @click="$parent.selected = 'personalInfo'"
                         :style="($parent.selected === 'personalInfo') ? {backgroundColor: '#eeeeee'} : ''">اطلاعات شخصی
                    </div>
                    <div class="option-1 w-100 d-flex align-items-center" @click="$parent.selected = 'contacts'"
                         :style="($parent.selected === 'contacts') ? {backgroundColor: '#eeeeee'} : ''">مخاطبان
                    </div>
                    <div class="option-1 w-100 d-flex align-items-center" @click="$parent.selected = 'locationInfo'"
                         :style="($parent.selected === 'locationInfo') ? {backgroundColor: '#eeeeee'} : ''">اطلاعات
                        مکانی و
                        ضربان قلب
                    </div>
                </div>
                <p v-on:click="$parent.logout" class="exit-btn">خروج</p>
            </div>
            <div class="app-overlay" @click="showMenu = false"></div>
        </div>
        <div style="padding: 12px">
            <div v-if="$parent.selected === 'personalInfo'" class="box w-100 d-flex flex-column">
                <div class="title">نام</div>
                <input class="user-input" v-model="$parent.firstName">
                <p style="color: red">{{ $parent.fields_errors.firstname }}</p>
                <div class="title">نام خانوادگی</div>
                <input class="user-input" v-model="$parent.lastName">
                <p style="color: red">{{ $parent.fields_errors.lastname }}</p>
                <div class="title">شماره موبایل</div>
                <input class="user-input" v-model="$parent.phoneNumber">
                <p style="color: red">{{ $parent.fields_errors.phone }}</p>
                <div class="title">ایمیل</div>
                <input class="user-input" v-model="$parent.email">
                <p style="color: red">{{ $parent.fields_errors.email }}</p>
                <div class="title">تاریخ تولد</div>
                <input class="user-input" v-model="$parent.birthDate">
                <p style="color: red">{{ $parent.fields_errors.birthday }}</p>
                <div class="title">جنسیت</div>
                <input class="user-input" v-model="$parent.gender">
                <p style="color: red">{{ $parent.fields_errors.gender }}</p>
                <div class="title">نام کاربری</div>
                <input class="user-input" v-model="$parent.username">
                <p style="color: red">{{ $parent.fields_errors.username }}</p>
                <div class="title">کد ساعت</div>
                <input class="user-input" v-model="$parent.watchId">
                <p style="color: red">{{ $parent.fields_errors.watch_code }}</p>
                <div class="title">رمز عبور</div>
                <input class="user-input" type="password" v-model="$parent.password">
                <p style="color: red">{{ $parent.fields_errors.password }}</p>
                <div class="title">تکرار رمز عبور</div>
                <input class="user-input" type="password" v-model="$parent.passwordConfirm">
                <p style="color: red">{{ $parent.fields_errors.password_confirm }}</p>
                <div class="w-100 d-flex flex-row justify-content-between align-items-center">
                    <div v-on:click="$parent.updateContacts" class="option d-flex justify-content-center align-items-center"
                         style="background-color: #111E6c; color: white;">تایید</div>
                </div>
            </div>
            <div v-else-if="$parent.selected === 'contacts'" class="box w-100 d-flex flex-column">
                <div class="title">نام مخاطب اول</div>
                <input class="user-input" v-model="$parent.contactOne">
                <p style="color: red">{{ $parent.fields_errors.contact_1 }}</p>
                <div class="title">شماره مخاطب اول</div>
                <input class="user-input" v-model="$parent.phoneOne">
                <p style="color: red">{{ $parent.fields_errors.phone_1 }}</p>
                <div class="title">نام مخاطب دوم</div>
                <input class="user-input" v-model="$parent.contactTwo">
                <p style="color: red">{{ $parent.fields_errors.contact_2 }}</p>
                <div class="title">شماره مخاطب دوم</div>
                <input class="user-input" v-model="$parent.phoneTwo">
                <p style="color: red">{{ $parent.fields_errors.phone_2 }}</p>
                <div class="title">نام مخاطب سوم</div>
                <input class="user-input" v-model="$parent.contactThree">
                <p style="color: red">{{ $parent.fields_errors.contact_3 }}</p>
                <div class="title">شماره مخاطب سوم</div>
                <input class="user-input" v-model="$parent.phoneThree">
                <p style="color: red">{{ $parent.fields_errors.phone_3 }}</p>
                <div class="title">نام مخاطب چهارم</div>
                <input class="user-input" v-model="$parent.contactFour">
                <p style="color: red">{{ $parent.fields_errors.contact_4 }}</p>
                <div class="title">شماره مخاطب چهارم</div>
                <input class="user-input" v-model="$parent.phoneFour">
                <p style="color: red">{{ $parent.fields_errors.phone_4 }}</p>
                <div class="title">نام مخاطب پنجم</div>
                <input class="user-input" v-model="$parent.contactFive">
                <p style="color: red">{{ $parent.fields_errors.contact_5 }}</p>
                <div class="title">شماره مخاطب پنجم</div>
                <input class="user-input" v-model="$parent.phoneFive">
                <p style="color: red">{{ $parent.fields_errors.phone_5 }}</p>
                <div class="w-100 d-flex flex-row justify-content-end align-items-center">
                    <div v-on:click="$parent.updateContacts" class="option d-flex justify-content-center align-items-center"
                         style="background-color: #111E6c; color: white;">تایید</div>
                </div>
            </div>
            <div v-else class="box w-100 d-flex flex-column">
                <div class="W-100 d-flex flex-column">
                    <div class="big-title">مشخصات مکانی</div>
                    <div class="user-input box-1 w-100"></div>
                </div>
                <div class="W-100 d-flex flex-column">
                    <div class="big-title">ضربان قلب</div>
                    <div class="user-input box-2 w-100 d-flex flex-column">
                        <iframe style="border: 1px solid #cccccc; Border-radius: 10px;
                        Overflow: hidden; width:100%; height: 100%;"
                                src="https://thingspeak.com/channels/1722465/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15">
                        </iframe>
                        <iframe style="border: 1px solid #cccccc; Border-radius: 10px;
                        Overflow: hidden; width:100%; height: 100%;"
                                src="https://thingspeak.com/channels/1722465/widgets/455567">
                        </iframe>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "MobilePanel",
    data() {
        return {
            showMenu: false
        }
    }
}
</script>

<style scoped>
.header {
    background-color: white;
    box-shadow: 0 5px 15px 5px rgba(0, 0, 0, 0.1);
    padding: 8px 12px;
    z-index: 1;
}

.mdi-watch, .mdi-menu {
    font-size: 20px;
}

.option {
    font-size: 16px;
    padding: 4px 8px;
    min-width: 0;
}

.body {
    padding: 16px 12px;
}

.nav-bar {
    height: 100%;
    border-radius: 20px 0 0 20px;
    background-color: white;
    box-shadow: 0 1px 7px 8px rgba(0, 0, 0, 0.06);
    padding: 36px 0 36px 24px;
    position: fixed;
    top: 0;
    right: 0;
    z-index: 3;
}


.big-title-1 {
    font-size: 18px;
    margin-bottom: 12px;
    text-align: center;
}

.option-1 {
    cursor: pointer;
    border-radius: 20px 0 0 20px;
    font-size: 18px;
    padding: 8px 12px;
    margin-bottom: 12px;
}

.exit-btn {
    font-size: 18px;
    width: fit-content;
    background-color: whitesmoke;
    color: firebrick;
    padding: 20px 24px 20px 34px;
    border-radius: 20px 0 0 20px;
    cursor: pointer;
}

.box {
    margin-bottom: 12px;
    padding: 4px;
}

.app-overlay {
    position: fixed; /* Sit on top of the page content */
    width: 100%; /* Full width (cover the whole page) */
    height: 100%; /* Full height (cover the whole page) */
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 2;
    background-color: rgba(0, 0, 0, 0.3); /* Black background with opacity */
}
</style>