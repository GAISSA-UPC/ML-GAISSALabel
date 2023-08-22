<template>
    <span style="width: 100%; display: flex; justify-content: space-between">
        <div style="display: flex; align-items: center">
            <el-button @click="canviCollapse" class="action-button-light">
                <font-awesome-icon :icon="['fas', 'bars']" />
            </el-button>
            <el-image
                src="https://gaissa.upc.edu/en/shared/GAISSALOGO.png/@@images/9e425bf5-ac52-418a-84fa-719ae8fedbf8.png"
                style="cursor:pointer; max-width: 40px; margin-left: 20px; margin-right: 5px"
                @click="obrirLink"
            />
            <span class="text-large font-600 mr-3"> Tool's name :) </span>
        </div>
        <div>
            <el-button color="var(--gaissa_green)" class="ml-2">{{ $t('Admin') }}</el-button>
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
