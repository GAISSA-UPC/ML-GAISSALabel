<template>
    <div class="background">
        <el-alert v-if="estat === 'login-ko-username'" :title="$t('The username does not match any of the existent user\'s one')" type="error" @close="estat = ''"/>
        <el-alert v-else-if="estat === 'login-ko-password'" :title="$t('Incorrect password')" type="error" @close="estat = ''"/>

        <el-card style="border-radius: 40px;width: 40vw;height: 80vh;">
            {{ $t('Administration Login') }}
            <el-form ref="loginForm" label-position="top">
                <el-form-item :label="$t('Username')" required>
                    <el-input v-model="username"/>
                </el-form-item>
                <el-form-item :label="$t('Password')" required>
                    <el-input
                        v-model="password"
                        type="password"
                    />
                </el-form-item>
                <el-form-item>
                    <el-button @click="login" color="var(--gaissa_green)">{{ $t('Login') }}</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script>
import usuaris from '@/services/usuaris'
export default {
    name: "AdminLogin",
    data() {
        return {
            msgErrorLogin: '',
            username: '',
            password: '',
            estat: '',
        };
    },
    methods: {
        async login() {
            const response = await usuaris.login(this.username, this.password)

            // Si tenim status i és 201 --> Login correcte i tenim token.
            if (response.status === 201) {
                console.log("hola")
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