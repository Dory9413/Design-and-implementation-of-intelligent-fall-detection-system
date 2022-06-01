<template>
<div class="body w-100 d-flex d-lg-none flex-column align-items-center">
    <div @click="$router.push('/')" class="w-50 d-flex flex-row justify-content-center align-items-center" style="margin-bottom: 24px">
        <i class="mdi mdi-watch iconstyle"></i>
        <div class="big-title">تکمیل اطلاعات</div>
    </div>
    <div class="box w-100 d-flex flex-column">
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
               style="background-color: lightslategray; color: white;">تایید</div>
        </div>
    </div>
</div>
</template>

<script>
export default {
    name: "MobileContacts"
}
</script>

<style scoped>
.mdi-watch {
    font-size: 50px;
}

.body {
    height: 100vh;
    padding: 16px !important;
}

.iconstyle:hover {
    color: #111E6c;
}

.user-input {
    margin-bottom: 12px;
}

.option {
    font-size: 18px;
    padding: 4px 12px;
    min-width: 0;
}
</style>