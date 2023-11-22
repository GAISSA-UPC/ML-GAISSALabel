<template>
    <div class="background">
        <div>
            <el-alert
                v-show="msgErrorLogin !== ''"
                class="mx-3 my-3"
                title="Error login"
                :description="msgErrorLogin"
                type="error"
                :closable="false"
            ></el-alert>
        </div>
        <div class="formStyle">
            <el-card
                style="border-radius: 40px;width: 40vw;height: 80vh;align-items: center"
            >
                <div class="text-center mt-3">{{ $t('Administration Login') }}</div>
                <el-form ref="loginForm" :model="loginForm" label-position="top">
                    <el-form-item :label="$t('Username')" required>
                        <el-input v-model="loginForm.username"></el-input>
                    </el-form-item>
                    <el-form-item :label="$t('Password')" required>
                        <el-input
                            v-model="loginForm.password"
                            type="password"
                        ></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button color="var(--gaissa_green)" @click="doLogin">{{ $t('Login') }}</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </div>
    </div>
</template>

<script>

import {ref} from 'vue';
//import {setToken} from '../utils/utilFunctions';
import { useRouter } from 'vue-router';

export default {

    name: "AdminLogin",

    data() {
        return {
            msgErrorLogin: '',
            loginForm: {
                username: '',
                password: '',
                admin: false,
            },
        };
    },

    setup() {
        const router = useRouter();

        let username = ref('');
        let password = ref('');
        let admin = ref(false);

        let msgErrorLogin = ref('');

        function setCookie(cname, cvalue, exdays) {
            const d = new Date();
            d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
            let expires = "expires="+d.toUTCString();
            document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
        }

        async function doLogin() {
            let data;
            let host = 'http://deploy-env.eba-6a6b2amf.us-west-2.elasticbeanstalk.com/';

            if (admin.value) {
                msgErrorLogin.value = '';

                let response = await fetch(host+"usuaris/login/admins/",  {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({username: username.value, password: password.value}),
                })
                let data = await response.json();
                console.log("data: ", data);
                if (data.non_field_errors) {
                    let str = '';
                    for (let string of data.non_field_errors) {
                        str += string + '\n';
                    }
                    msgErrorLogin.value = str;
                }
                else if (data.token) {
                    setCookie("Token", data.token, 1);
                    //setToken(data.token);
                    //redirect path --> /Review
                    router.push('/Review');
                }
            }
            else {
                msgErrorLogin.value = '';

                let response =  await fetch(host+"usuaris/login/organitzadors/",  {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({username: username.value, password: password.value}),
                })
                console.log("response: ", response);

                let data = await response.json();
                console.log("login org data: ", data);
                if (data.non_field_errors) {
                    let str = '';
                    for (let string of data.non_field_errors) {
                        str += string + '\n';
                    }
                    msgErrorLogin.value = str;
                }
                else if (data.token) {
                    setCookie("Token", data.token, 1);
                    //document.cookie = `${data.token}; max-age=${60000 * 30};`;
                    //setToken(data.token);
                    //redirect path  --> /edit
                    router.push('/edit');
                }
            }

        }

        return {
            username,
            password,
            admin,
            msgErrorLogin,
            doLogin
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