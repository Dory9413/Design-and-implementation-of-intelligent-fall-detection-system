<template>
    <div id="app" class="w-100">
        <router-view/>
    </div>
</template>

<style>
@import './assets/main.css';
@import '~bootstrap/dist/css/bootstrap.css';
@import './assets/fonts/iranyekan.css';

body {
    margin: 0;
    overflow-x: hidden;
    direction: rtl;
    font-family: iran_yekan, Helvetica;
    color: #333;
    background-color: whitesmoke;
    cursor: default;
    background-image: url('./assets/blue.jpg');
    background-size: 50%;
}

.router-link-active, .router-link-exact-active, a {
    text-decoration: none;
    color: inherit;
}
</style>
