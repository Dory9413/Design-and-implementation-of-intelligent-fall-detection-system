<template>
    <div class="body d-flex f-lg-none flex-column align-items-center justify-content-center">
        <div @click="$router.push('/')" class="w-50 d-flex flex-row justify-content-center align-items-center" style="margin-bottom: 24px">
            <i class="mdi mdi-watch iconstyle"></i>
            <div class="big-title">ورود</div>
        </div>
        <div class="w-100 d-flex justify-content-center align-items-center">
            <div class="box w-100 d-flex flex-column">
                <div class="title">نام کاربری</div>
                <input class="user-input" v-model="$parent.username">
                <p style="color: red;">{{ $parent.fields_errors.username }}</p>
                <div class="title">رمز عبور</div>
                <input class="user-input" type="password" v-model="$parent.password">
                <p style="color: red;">{{ $parent.fields_errors.password }}</p>
                <p style="white-space: pre; color: red;">{{ $parent.response_code }}</p>
                <div class="w-100 d-flex flex-row justify-content-between align-items-center">
                    <div v-on:click="$parent.login" class="option d-flex justify-content-center align-items-center">ورود</div>
                    <router-link to="/signup" class="option d-flex justify-content-center align-items-center">ثبت
                        نام
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "MobileLogin"
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