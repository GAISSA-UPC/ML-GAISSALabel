<template>
    <el-menu
        :default-active="activeRoute"
        class="el-menu-vertical"
        :collapse="collapsed"
        style="margin-left: 13px; margin-right: 10px"
    >
        <el-menu-item index="home" @click="$router.push({name: 'home'})">
            <font-awesome-icon :icon="['fas', 'house']" class="icon"/>
            <template #title>{{ $t('Home') }}</template>
        </el-menu-item>
        <el-sub-menu index="1">
            <template #title>
                <font-awesome-icon :icon="['fas', 'dumbbell']" class="icon"/>
                <span>{{ $t('Training') }}</span>
            </template>
            <el-menu-item index="training form" @click="$router.push({name: 'training form'})">
                {{ $t('Form') }}
            </el-menu-item>
            <el-menu-item index="training pre saved" @click="$router.push({name: 'training pre saved'})">
                {{ $t('Database') }}
            </el-menu-item>
            <el-menu-item index="1-3">{{ $t('File') }}</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="2">
            <template #title>
                <font-awesome-icon :icon="['fas', 'bullseye']" class="icon"/>
                <span>{{ $t('Inference') }}</span>
            </template>
            <el-menu-item index="inference form" @click="$router.push({name: 'inference form'})">
                {{ $t('Form') }}
            </el-menu-item>
            <el-menu-item index="inference pre saved" @click="$router.push({name: 'inference pre saved'})">
                {{ $t('Database') }}
            </el-menu-item>
            <el-menu-item index="2-3">{{ $t('File') }}</el-menu-item>
            <el-menu-item index="2-4">{{ $t('Deployment') }}</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="3">
            <font-awesome-icon :icon="['fas', 'people-group']" class="icon"/>
            <template #title>{{ $t('About') }}</template>
        </el-menu-item>
    </el-menu>
</template>

<script>
export default {
    name: "MenuLateral",
    props: {
        collapsed: {required: false, type: Boolean, default: false}
    },
    data() {
        return {
            activeRoute: this.$route.name,
        };
    },
    watch: {
        $route(to) {
            this.activeRoute = to.name
        }
    }
}
</script>

<style>
.el-menu-vertical:not(.el-menu--collapse) {
    width: 200px;
}
.el-menu-vertical {
    min-height: 95%;
}
.el-menu-item.is-active {
    color: var(--gaissa_green)
}
.icon {
    width: 20px;
    margin-right: 10px;
}
</style>
