<template>
    <div class="body d-flex f-lg-none flex-column align-items-center">
        <div @click="$router.push('/')" class="d-flex flex-row justify-content-center align-items-center">
            <i class="mdi mdi-watch iconstyle"></i>
            <div class="big-title">ثبت نام</div>
        </div>
        <div class="box w-100 d-flex flex-column">
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
                <router-link to="/login" class="option d-flex justify-content-center align-items-center">ورود
                </router-link>
                <div v-on:click="$parent.signUp"
                   class="option d-flex justify-content-center align-items-center buttonstyle">ثبت نام</div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "MobileSignup"
}
</script>

<style scoped>
.mdi-watch {
    font-size: 50px;
}

.body {
    height: 100vh;
    padding: 16px;
}

.box {
    margin-bottom: 12px;
    padding: 4px;
}

.iconstyle:hover {
    color: #111E6c;
}

.user-input {
    margin-bottom: 12px;
}

.option {
    font-size: 18px;
    padding: 4px 8px;
    min-width: 0;
}
</style>