<template>
    <span style="width: 100%; display: flex; justify-content: space-between">
        <div style="display: flex; align-items: center">
            <el-button @click="canviCollapse" class="action-button-light">
                <font-awesome-icon :icon="['fas', 'bars']" />
            </el-button>
            <el-image
                src="https://gaissa.upc.edu/en/shared/GAISSALOGO.png/@@images/image-1600-06666a1dbbeb6508fe3df5dd86092b2c.png"
                style="cursor:pointer; max-width: 40px; margin-left: 20px; margin-right: 5px"
                @click="obrirLink"
            />
            <span class="text-large font-600 mr-3" style="color: var(--gaissa_green);font-weight: bold"> GAISSA Label </span>
        </div>
        <div>
            <el-button v-if="$store.getters.isLogged" color="var(--gaissa_green)" class="ml-2" @click="$router.push({name: 'home'});$store.commit('logout')">{{ $t('Log out') }}</el-button>
            <el-button v-else color="var(--gaissa_green)" class="ml-2" @click="$router.push({name: 'Admin login'})">{{ $t('Admin') }}</el-button>
        </div>
    </span>
</template>

<script>
export default {
    name: "BarraSuperior",
    props: {
        collapsed: {required: false, type: Boolean, default: false}
    },
    emits: ['collapse', 'expand'],
    methods: {
        obrirLink() {
            window.open('https://gaissa.upc.edu/en', '_blank');
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
