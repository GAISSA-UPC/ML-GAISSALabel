<template>
    <div class="background">
        <el-alert v-if="estat === 'login-ko-buit'" :title="$t('Please, enter username and password')" type="error" @close="estat = ''"/>
        <el-alert v-else-if="estat === 'login-ko-username'" :title="$t('There is no administrator with such username')" type="error" @close="estat = ''"/>
        <el-alert v-else-if="estat === 'login-ko-password'" :title="$t('Incorrect password')" type="error" @close="estat = ''"/>

        <br>

        <div>
            <v-card
                height="500"
                width="500"
                color="#C0D8AF60"
                style="border-radius: 40px;"
            >
                <v-card-title class="text-center mt-3">{{ $t('Administrator login') }}</v-card-title>
                <v-card-text>
                    <v-text-field v-model="username" :label="$t('Username')" required style="margin-top: 100px;"></v-text-field>
                    <v-text-field @keydown.enter="login()" v-model="password" :label="$t('Password')" type="password" required style="margin-top: 30px;"></v-text-field>
                    <el-button @click="login()" color="var(--gaissa_green)" class="mx-auto d-block mt-16" style="font-size: medium" >{{ $t('Login') }}</el-button>
                </v-card-text>
            </v-card>
        </div>
    </div>
</template>

<script>
import usuaris from '@/controllers/usuaris'
export default {
    name: "AdminLogin",
    data() {
        return {
            username: '',
            password: '',
            estat: '',
        };
    },
    methods: {
        async login() {
            const response = await usuaris.login(this.username, this.password)

            // Username i contrasenya han d'estar omplerts
            if (!this.username || !this.password) {
                this.estat = 'login-ko-buit'
            }

            // Si tenim status i és 201 --> Login correcte i tenim token.
            else if (response.status === 201) {
                this.$store.dispatch("auth/login", response.data['token'])
                this.$router.push({name: 'Admin tools'})
            }

            // Si no, vol dir que rebem el error. Si status és 404 --> username no trobat.
            else if (response.response.status === 404) {
                this.estat = 'login-ko-username'
            }

            // Si no, vol dir que rebem error i si status és 400 --> La contrasenya no és correcta.
            else {
                this.estat = 'login-ko-password'
            }
        }
    }
}
</script>

<style scoped>

.background {
    height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.formStyle {
    display: flex;
    justify-content: center;
    margin-top: auto;
    margin-bottom: auto;
}

</style>