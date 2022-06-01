<template>
    <div class="w-100 d-flex d-lg-none flex-column">
        <div class="header w-100 d-flex flex-row justify-content-between align-items-center">
            <div class="d-flex flex-row align-items-center">
                <i class="mdi mdi-watch"></i>
                <router-link to="/panel" class="option d-flex justify-content-center align-items-center">حساب کاربری
                </router-link>
            </div>
            <div class="d-flex flex-row align-items-center">
                <router-link to="/login" class="option d-flex justify-content-center align-items-center">ورود
                </router-link>
                <router-link to="/signup" class="option d-flex justify-content-center align-items-center">ثبت‌نام
                </router-link>
            </div>
        </div>
        <div class="body w-100 d-flex flex-column">
            <div class="box w-100 d-flex flex-row">
                <div class="mini-box w-25 d-flex justify-content-center align-items-center img1tabli"></div>
                <div class="mini-box w-75 d-flex justify-content-center align-items-center img2tabli"></div>
            </div>
            <div class="box w-100 d-flex flex-column" style="padding-left: 12px">
                <div class="mini-box w-100 d-flex justify-content-center align-items-center img3tabli"></div>
                <div class="w-100 d-flex flex-column" style="margin: 4px">
                    <div class="title" style="text-align: center">سنسور پوشیدنی هوشمند با قابلیت تشخیص افتادن</div>
                    <div class="sub-title" style="text-align: center">
                        با افزایش تعداد افراد مسن در جامعه، اهمیت نگهداری و سلامت آن‌ها نیز افزایش می‌یابد.
                        از آنجایی که افتادن یکی از عوامل بستری شدن این افراد به شمار می‌رود، خرید یک سنسور پوشیدنی
                        هوشمند که بتواند
                        افتادن را تشخیص دهد و به خانواده او پیام ارسال کند را پیشنهاد می‌دهیم!
                        با استفاده از این سنسور با خیال آسوده به عزیزان سالمند خود اجازه دهید به تنهایی پیاده‌روی
                        روند و دیگر نگران سلامتی آن‌ها
                        نباشید. این سنسور پوشیدنی قابلیت ارسال موقعیت مکانی و ضربان قلب فرد را از طریق پیامک دارا
                        بوده و به این علت به سرعت اطلاع رسانی لازم را به عمل می‌آورد.
                    </div>
                </div>
            </div>
            <div class="box w-100 d-flex flex-column justify-content-center align-items-center">
                <div class="title">درباره‌ی ما</div>
                <div class="sub-title w-50" style="text-align: center">
                    تیم دانشکده مهندسی کامپیوتر امیرکبیر مفتخر است این ساعت هوشمند با قابلیت افتادن را ارائه دهد.
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "MobileMain"
}
</script>

<style scoped>
.header {
    background-color: white;
    box-shadow: 0 5px 15px 5px rgba(0, 0, 0, 0.1);
    padding: 8px 12px;
    z-index: 1;
}

.mdi-watch {
    color: #111E6c;
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

.img1tabli {
    background-image: url('../../assets/w7.jpg');
    background-size: cover;
}

.img2tabli {
    background-image: url('../../assets/w4.jpg');
    background-size: cover;
    background-position: center;
}

.box {
    margin-bottom: 12px;
    padding: 4px;
}

.img3tabli {
    background-image: url('../../assets/w3.jpg');
    background-size: cover;
}

.mini-box {
    background-color: whitesmoke;
    border-radius: 10px;
    margin: 4px;
    height: 30vw;
}
</style>