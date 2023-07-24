<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                <BarraSuperior/>
            </el-header>
            <el-container>
                <el-aside width="200px">
                    <MenuLateral/>
                </el-aside>
                <el-main>
                    <RouterView />
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script setup>
import 'element-plus/theme-chalk/index.css'
import { RouterView } from 'vue-router'
import MenuLateral from "@/components/base/MenuLateral.vue";
import BarraSuperior from "@/components/base/BarraSuperior.vue";
</script>

<style scoped>
header {
    line-height: 1.5;
}

nav {
    width: 100%;
    font-size: 12px;
    text-align: center;
    margin-top: 2rem;
}

nav a.router-link-exact-active {
    color: var(--color-text);
}

nav a.router-link-exact-active:hover {
    background-color: transparent;
}

nav a {
    display: inline-block;
    padding: 0 1rem;
    border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
    border: 0;
}

@media (min-width: 1024px) {
    header {
        display: flex;
        place-items: center;
        padding-right: calc(var(--section-gap) / 2);
    }

    header {
        display: flex;
        place-items: flex-start;
        flex-wrap: wrap;
    }

    nav {
        text-align: left;
        margin-left: -1rem;
        font-size: 1rem;

        padding: 1rem 0;
        margin-top: 1rem;
    }
}
</style>
