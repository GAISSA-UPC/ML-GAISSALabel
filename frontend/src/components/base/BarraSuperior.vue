<template>
    <span style="width: 100%; display: flex; align-items: center">
        <el-button>
            <font-awesome-icon :icon="['fas', 'bars']" />
        </el-button>
        <el-image
            src="https://gaissa.upc.edu/en/shared/GAISSALOGO.png/@@images/9e425bf5-ac52-418a-84fa-719ae8fedbf8.png"
            style="cursor:pointer; max-width: 40px"
            @click="obrirLink"
        />
        <span class="text-large font-600 mr-3"> Tool's name :) </span>
        <el-button type="primary" class="ml-2">{{ $t('Admin') }}</el-button>
    </span>
</template>

<script>
export default {
    name: "BarraSuperior",
    methods: {
        obrirLink() {
            window.open('https://gaissa.upc.edu/en', '_blank');
        }
    }
}
</script>

<style scoped>

</style>