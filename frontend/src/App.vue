<template>
    <div class="common-layout">
        <el-container class="app-container">
            <el-header style="display: flex; align-items: center">
                <BarraSuperior
                    :collapsed="collapse"
                    @collapse="collapse=true"
                    @expand="collapse=false"
                />
            </el-header>
            <el-container class="main-container" :class="{ 'mobile': isMobile }">
                <el-aside :class="{ 'mobile': isMobile }" :width="isMobile ? 'auto' : (collapse ? '64px' : '200px')">
                    <MenuLateral
                        :collapsed="collapse"
                        :class="{ 'mobile': isMobile }"
                    />
                </el-aside>
                <el-main :class="{ 'mobile': isMobile }" style="margin-right: 75px">
                    <RouterView />
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script>
import { RouterView } from 'vue-router'
import MenuLateral from "@/components/base/MenuLateral.vue";
import BarraSuperior from "@/components/base/BarraSuperior.vue";

export default {
    name: "App",
    components: {
        RouterView, 
        MenuLateral, 
        BarraSuperior,
    },
    data() {
        return {
            collapse: false,
            isMobile: false
        }
    },
    mounted() {
        this.checkScreenSize()
        window.addEventListener('resize', this.checkScreenSize)
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.checkScreenSize)
    },
    methods: {
        checkScreenSize() {
            this.isMobile = window.innerWidth < 768
            this.collapse = this.isMobile
        }
    }
}</script>

<style scoped>
.app-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.main-container {
    flex: 1;
    display: flex;
}

.main-container.mobile {
    flex-direction: column;
}

.el-aside.mobile {
    width: 100% !important;
    max-height: fit-content;
}

.el-main.mobile {
    margin-right: 0 !important;
    padding: 20px;
}

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
