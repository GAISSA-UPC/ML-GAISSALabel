<template>
    <span style="width: 100%; display: flex; justify-content: space-between">
        <div style="display: flex; align-items: center">
            <el-button @click="canviCollapse" class="action-button-light">
                <font-awesome-icon :icon="['fas', 'bars']" />
            </el-button>
            <el-image
                src="/gaissalogo_small.webp"
                alt="GAISSA logo"
                style="cursor:pointer; max-width: 40px; margin-left: 20px; margin-right: 5px"
                @click="obrirLink"
            />
            <span class="text-large font-600 mr-3" style="color: var(--gaissa_green);font-weight: bold"> GAISSA Label </span>
        </div>
        <div>
            <el-button v-if="isLogged" color="var(--gaissa_green)" class="ml-2" @click="logout">{{ $t('Log out') }}</el-button>
            <el-button v-else color="var(--gaissa_green)" class="ml-2" @click="$router.push({name: 'Admin login'})">{{ $t('Admin') }}</el-button>
        </div>
    </span>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: "BarraSuperior",
    props: {
        collapsed: {required: false, type: Boolean, default: false}
    },
    emits: ['collapse', 'expand'],
    computed: {
        ...mapGetters({
            isLogged: 'auth/isLogged'
        })
    },
    methods: {
        obrirLink() {
            window.open('https://gaissa.upc.edu/en', '_blank');
        },
        logout() {
            this.$store.dispatch('auth/logout');
            this.$router.push({name: 'home'});
        },
        canviCollapse(event) {
            if (this.collapsed) {
                this.$emit('expand')
            } else {
                this.$emit('collapse')
            }
            event.target.blur()
        }
    }
}
</script>
