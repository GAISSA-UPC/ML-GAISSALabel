<template>
    <div class="admin-login-page">
        <!-- Alert Messages -->
        <div class="alerts-container">
            <el-alert 
                v-if="estat === 'login-ko-buit'" 
                :title="$t('Please, enter username and password')" 
                type="error" 
                @close="estat = ''"
                show-icon
            />
            <el-alert 
                v-else-if="estat === 'login-ko-username'" 
                :title="$t('There is no administrator with such username')" 
                type="error" 
                @close="estat = ''"
                show-icon
            />
            <el-alert 
                v-else-if="estat === 'login-ko-password'" 
                :title="$t('Incorrect password')" 
                type="error" 
                @close="estat = ''"
                show-icon
            />
        </div>

        <!-- Login Card -->
        <div class="login-container">
            <div class="login-card">
                <!-- Logo Section -->
                <div class="logo-section">
                    <img src="/gaissalogo_small.webp" alt="GAISSA Tools" class="gaissa-logo" />
                    <h1 class="login-title">{{ $t('Administrator Login') }}</h1>
                    <p class="login-subtitle">{{ $t('Access GAISSA Tools Administration Panel') }}</p>
                </div>

                <!-- Form Section -->
                <form @submit.prevent="login()" class="login-form">
                    <div class="form-group">
                        <label for="username" class="form-label">{{ $t('Username') }}</label>
                        <input 
                            id="username"
                            v-model="username" 
                            type="text"
                            class="form-input"
                            :placeholder="$t('Enter your username')"
                            required
                        />
                    </div>
                    
                    <div class="form-group">
                        <label for="password" class="form-label">{{ $t('Password') }}</label>
                        <input 
                            id="password"
                            v-model="password" 
                            type="password"
                            class="form-input"
                            :placeholder="$t('Enter your password')"
                            @keydown.enter="login()"
                            required
                        />
                    </div>

                    <button type="submit" class="login-button">
                        {{ $t('Login') }}
                    </button>
                </form>
            </div>
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
.admin-login-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    margin-top: 20px;
}

.alerts-container {
    position: fixed;
    top: 60px;
}

.login-container {
    position: relative;
    z-index: 10;
}

.login-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 40px;
    width: 100%;
    max-width: 450px;
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.1),
        0 0 0 1px rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
}

.login-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--gaissa_green), #3498db, var(--gaissa_green));
}

.logo-section {
    text-align: center;
    margin-bottom: 40px;
}

.gaissa-logo {
    width: 80px;
    height: 80px;
    margin-bottom: 20px;
}

.login-title {
    color: var(--gaissa_green);
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 8px 0;
}

.login-subtitle {
    color: #5a6c7d;
    font-size: 1rem;
    margin: 0;
    font-weight: 400;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-label {
    color: #2c3e50;
    font-weight: 600;
    font-size: 0.9rem;
    margin: 0;
}

.form-input {
    padding: 16px 20px;
    border: 2px solid #e1e5e9;
    border-radius: 12px;
}

.form-input:focus {
    outline: none;
    border-color: var(--gaissa_green);
}

.login-button {
    background: var(--gaissa_green);
    color: white;
    padding: 16px 24px;
    border: none;
    border-radius: 12px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    margin-top: 8px;
    position: relative;
}

.login-button:hover {
    border: 1px solid var(--gaissa_green);
}


@media (max-width: 1359px) {
    .admin-login-page {
        padding: 15px;
    }
    
    .login-card {
        padding: 30px 25px;
        max-width: 100%;
    }
    
    .login-title {
        font-size: 1.75rem;
    }
    
    .gaissa-logo {
        width: 60px;
        height: 60px;
    }
    
    .alerts-container {
        top: 120px;
    }
}

</style>