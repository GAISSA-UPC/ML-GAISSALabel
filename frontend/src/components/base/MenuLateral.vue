<template>
    <el-menu
        default-active="0"
        class="el-menu-vertical"
        :collapse="collapsed"
        @open="handleOpen"
        @close="handleClose"
        style="margin-left: 13px; margin-right: 10px"
    >
        <el-menu-item index="0">
            <font-awesome-icon :icon="['fas', 'house']" class="icon"/>
            <template #title>{{ $t('Home') }}</template>
        </el-menu-item>
        <el-sub-menu index="1">
            <template #title>
                <font-awesome-icon :icon="['fas', 'dumbbell']" class="icon"/>
                <span>{{ $t('Training') }}</span>
            </template>
            <el-menu-item index="1-1">{{ $t('Form') }}</el-menu-item>
            <el-menu-item index="1-2">{{ $t('Database') }}</el-menu-item>
            <el-menu-item index="1-3">{{ $t('File') }}</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="2">
            <template #title>
                <font-awesome-icon :icon="['fas', 'bullseye']" class="icon"/>
                <span>{{ $t('Inference') }}</span>
            </template>
            <el-menu-item index="2-1">{{ $t('Form') }}</el-menu-item>
            <el-menu-item index="2-2">{{ $t('Database') }}</el-menu-item>
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
    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath)
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath)
        }
    }
}
</script>

<style>
.el-menu-vertical:not(.el-menu--collapse) {
    width: 200px;
    min-height: 90%;
}
.el-menu-item.is-active {
    color: var(--gaissa_green)
}
.icon {
    width: 20px;
    margin-right: 10px;
}
</style>
