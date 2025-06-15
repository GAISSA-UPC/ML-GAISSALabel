<template>
    <el-menu
        :default-active="activeRoute"
        class="el-menu-vertical"
        :collapse="collapsed"
        style="margin-left: 10px; margin-right: 10px"
    >
        <el-menu-item index="home" @click="$router.push({name: 'home'})">
            <font-awesome-icon :icon="['fas', 'house']" class="icon"/>
            <template #title>{{ $t('Home') }}</template>
        </el-menu-item>
        <el-sub-menu index="1" v-if="isGAISSALabelEnabled">
            <template #title>
                <font-awesome-icon :icon="['fas', 'tag']" class="icon"/>
                <span>{{ $t('GAISSALabel') }}</span>
            </template>
            <el-menu-item index="gaissalabel-home" @click="$router.push({name: 'gaissalabel-home'})">
                {{ $t('Home') }}
            </el-menu-item>
            <el-sub-menu index="1-1">
                <template #title>
                    <font-awesome-icon :icon="['fas', 'dumbbell']" class="icon"/>
                    <span>{{ $t('Training') }}</span>
                </template>
                <el-menu-item index="training form" @click="$router.push({name: 'training form'})">
                    {{ $t('New from Form') }}
                </el-menu-item>
                <el-menu-item index="training file" @click="$router.push({name: 'training file'})">
                    {{ $t('New from File') }}
                </el-menu-item>
                <el-menu-item index="training pre saved" @click="$router.push({name: 'training pre saved'})">
                    {{ $t('Consult') }}
                </el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="1-2">
                <template #title>
                    <font-awesome-icon :icon="['fas', 'bullseye']" class="icon"/>
                    <span>{{ $t('Inference') }}</span>
                </template>
                <el-menu-item index="inference form" @click="$router.push({name: 'inference form'})">
                    {{ $t('New from Form') }}
                </el-menu-item>
                <el-menu-item index="inference file" @click="$router.push({name: 'inference file'})">
                    {{ $t('New from File') }}
                </el-menu-item>
                <el-menu-item index="inference deploy" @click="$router.push({name: 'inference deploy'})">
                    {{ $t('New from Deployment') }}
                </el-menu-item>
                <el-menu-item index="inference pre saved" @click="$router.push({name: 'inference pre saved'})">
                    {{ $t('Consult') }}
                </el-menu-item>
            </el-sub-menu>
        </el-sub-menu>
        <el-sub-menu index="2" v-if="isGAISSAROIAnalyzerEnabled">
            <template #title>
                <font-awesome-icon :icon="['fas', 'chart-line']" class="icon"/>
                <span class="wrap-title">{{ $t('GAISSA ROI Analyzer') }}</span>
            </template>
            <el-menu-item index="GAISSA ROI Analyzer Research Repository" @click="$router.push({name: 'GAISSA ROI Analyzer Research Repository'})">
                {{ $t('Research Analyses') }}
            </el-menu-item>
            <el-menu-item index="GAISSA ROI Analyzer Calculation Repository" @click="$router.push({name: 'GAISSA ROI Analyzer Calculation Repository'})">
                {{ $t('Saved Analyses') }}
            </el-menu-item>
            <el-menu-item index="GAISSA ROI Analyzer New Form" @click="$router.push({name: 'GAISSA ROI Analyzer New Form'})">
                {{ $t('Calculate ROI') }}
            </el-menu-item>
            <el-menu-item index="GAISSA ROI Analyzer Comparison" @click="$router.push({name: 'GAISSA ROI Analyzer Comparison'})">
                {{ $t('Compare Analyses') }}
            </el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="3" v-if="isLogged">
            <template #title>
                <font-awesome-icon :icon="['fas', 'screwdriver-wrench']" class="icon"/>
                <span>{{ $t('Administration') }}</span>
            </template>
            <el-menu-item index="Admin tools" @click="$router.push({name: 'Admin tools'})">
                {{ $t('Tools Configuration') }}
            </el-menu-item>
            <el-menu-item index="Admin sincronitzacio" v-if="isGAISSALabelEnabled" @click="$router.push({name: 'Admin sincronitzacio'})">
                {{ $t('Synchronization') }}
            </el-menu-item>
            <el-menu-item index="Admin mètriques i informacions" v-if="isGAISSALabelEnabled" @click="$router.push({name: 'Admin mètriques i informacions'})">
                {{ $t('Metrics') }}
            </el-menu-item>
            <el-menu-item index="Admin eines" v-if="isGAISSALabelEnabled" @click="$router.push({name: 'Admin eines'})">
                {{ $t('Calculation tools') }}
            </el-menu-item>
        </el-sub-menu>
        <el-menu-item index="about" @click="$router.push({name: 'about'})">
            <font-awesome-icon :icon="['fas', 'people-group']" class="icon"/>
            <template #title>{{ $t('About') }}</template>
        </el-menu-item>
    </el-menu>
</template>

<script>
import { mapGetters } from 'vuex';

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
    computed: {
        ...mapGetters({
            isGAISSALabelEnabled: 'configuration/isGAISSALabelEnabled',
            isGAISSAROIAnalyzerEnabled: 'configuration/isGAISSAROIAnalyzerEnabled',
            isConfigLoaded: 'configuration/isConfigLoaded',
            isLogged: 'auth/isLogged'
        })
    },
    watch: {
        $route(to) {
            this.activeRoute = to.name
        }
    },
    async mounted() {
        // Only fetch if not already loaded
        if (!this.isConfigLoaded) {
            await this.$store.dispatch('configuration/fetchConfiguration');
        }
    }
}
</script>

<style>
.el-menu-vertical:not(.el-menu--collapse) {
    width: 200px;
}

.el-menu-vertical {
    min-height: 98%;
}

.el-menu-vertical.mobile {
    width: 100% !important;
    min-height: auto;
    margin: 0 !important;
}

.el-menu-item.is-active {
    color: var(--gaissa_green)
}

.el-menu-item {
    white-space: normal !important;
    word-wrap: break-word;
    line-height: 1.4 !important;
}

.icon {
    width: 20px;
    margin-right: 10px;
}

.wrap-title {
    display: inline-block;
    text-align: left;
    line-height: 1.2;
    white-space: normal;
}

@media (max-width: 1339px) {
    .el-menu-vertical {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }

    .el-menu-vertical .el-menu-item,
    .el-menu-vertical .el-sub-menu__title {
        width: auto;
        min-width: 60px;
        text-align: center;
        padding: 0 20px;
    }
    
    .el-menu-vertical .el-menu-item .icon,
    .el-menu-vertical .el-sub-menu__title .icon {
        margin-right: 5px;
    }
    
    .el-menu-vertical .el-menu--popup {
        min-width: 60px;
    }

    .el-menu-vertical .el-menu--popup .el-menu-item {
        text-align: center;
        padding: 0 20px;
    }
}

@media (min-width: 1340px) {
    .el-menu-vertical {
        display: block;
    }

    .el-menu-vertical.el-menu--collapse {
        width: 64px !important;
    }
}
</style>