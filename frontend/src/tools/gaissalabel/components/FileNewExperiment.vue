<template>
    <h1>{{ $t("Energy label for") }} {{ fase }}</h1><br>
    <h2>{{ $t("Register a new") }} {{ fase }}</h2><br>

    <p style="font-size: 20px">{{ $t('This page allows you to evaluate the energy efficiency of your models\'') }} {{ fase }}s. {{ $t('You may upload the file or files that provide the information for the evaluation.') }}</p>
    <br>

    <div>
        <el-form label-position="top">
            <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("Files") }}</h3><br>
            <el-form-item>
                <el-upload
                    v-model:file-list="fileList"
                    multiple
                    drag
                    style="width: 100%"
                    :auto-upload="false"
                    :show-file-list="false"
                >
                    <font-awesome-icon :icon="['fas', 'cloud-arrow-up']" />
                    <div class="el-upload__text">
                        {{ $t('Drop file here or') }} <em>{{ $t('click to upload') }}</em>
                    </div>
                </el-upload>

                <ul class="el-upload-list el-upload-list--text" style="width: 100%">
                    <li v-for="(file, index) in fileList" :key="index" class="el-upload-list__item is-ready" tabindex="0">
                        <div class="el-upload-list__item-info">
                            <a class="el-upload-list__item-name">
                                <i class="el-icon el-icon--document">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                                        <path fill="currentColor" d="M832 384H576V128H192v768h640zm-26.496-64L640 154.496V320zM160 64h480l256 256v608a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V96a32 32 0 0 1 32-32m160 448h384v64H320zm0-192h160v64H320zm0 384h384v64H320z"></path>
                                    </svg>
                                </i>
                                <span class="el-upload-list__item-file-name" :title="file.name">{{ file.name }}</span>
                                <el-select style="margin-left: 10px" v-model="file.tool" :placeholder="$t('Tool used')" :clearable="true">
                                    <el-option v-for="eina in eines" :key="eina.nom" :label="eina.nom" :value="eina.id" />
                                </el-select>
                            </a>
                        </div>
                        <el-button class="el-icon el-icon--close" @click="fileList.splice(index, 1)">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                                <path fill="currentColor" d="M764.288 214.592 512 466.88 259.712 214.592a31.936 31.936 0 0 0-45.12 45.12L466.752 512 214.528 764.224a31.936 31.936 0 1 0 45.12 45.184L512 557.184l252.288 252.288a31.936 31.936 0 0 0 45.12-45.12L557.12 512.064l252.288-252.352a31.936 31.936 0 1 0-45.12-45.184z"></path>
                            </svg>
                        </el-button>
                    </li>
                </ul>
            </el-form-item>
            <el-button
                ref="generateLabelButton"
                @click="gestioFitxers"
                color="var(--gaissa_green)"
                v-show="fileList.length !== 0"
            >
                {{ $t('Generate label') }}
            </el-button>
        </el-form><br>
    </div><br>

    <h3 style="color: var(--gaissa_green);font-weight: bold">{{ $t("How to obtain the files?") }}</h3><br>

    <p style="font-size: 20px">{{ $t('There are many ways you can get the needed information. Here, we propose the following tools:') }}</p><br>

    <p style="font-weight: bold">{{ $t('GAISSALabel plug-in') }}</p>
    <p>{{ $t('We offer you a plug-in that runs on the terminal of your server. It will help you generate a file with the \
        configuration parameters of your model. Specifically, it will provide the size of the model, the size of its file and the FLOPS.') }}</p>
    <p>{{ $t('You can download it through this') }} <a href="/GAISSALabel_plugin.zip" target="_blank">{{ $t('link') }}</a>.</p>
    <p>{{ $t('Then, follow these steps:') }}</p>
    <ol style="margin-left: 30px">
        <li><p>{{ $t('Decompress the downloaded file') }}</p></li>
        <li><p>{{ $t('Access your console and go inside the decompressed folder') }}</p></li>
        <li><p>{{ $t('Create a python virtual environment using the command: # python -m venv env') }}</p></li>
        <li><p>{{ $t('Activate the virtual environment: # source env/bin/activate') }}</p></li>
        <li><p>{{ $t('Install the requirements: # pip install -r requirements.txt') }}</p></li>
        <li><p>{{ $t('Run the script and follow the instructions of the plug-in: # python main_script.py') }}</p></li>
    </ol><br>

    <p style="font-weight: bold">{{ $t('CodeCarbon') }}</p>
    <p>{{ $t('CodeCarbon will help you compute the information about the duration of your training or inference and the energy consumed.') }}</p>
    <p>{{ $t('To install and use this tool, you may:') }}</p>
    <ol style="margin-left: 30px">
        <li><p>{{ $t('Download CodeCarbon using this') }} <a href="https://github.com/mlco2/codecarbon" target="_blank">{{ $t('link') }}</a>.</p></li>
        <li><p>{{ $t('Follow the documentation of CodeCarbon to install and use the tool. The documentation is accessible') }} <a href="https://mlco2.github.io/codecarbon/" target="_blank">{{ $t('here') }}</a>.</p></li>
    </ol><br>


</template>

<script>
import eines from "@/tools/gaissalabel/services/eines";
export default {
    name: "FileNewExperiment",
    props: {
        fase: {required: true, type: String}
    },
    data() {
        return {
            estat: '',
            fileList: [],
            eines: null,
        };
    },
    methods: {
        async refrescaEines() {
            let response = await eines.list()
            this.eines = response.data
        },
        async gestioFitxers() {
            const info = await this.carregarFitxers()
            const nameRouter = (this.fase === this.$t('Training')) ? 'training form' : 'inference form'
            this.$router.push({
                name: nameRouter,
                query: {dadesInicials: JSON.stringify(info)}
            })
        },
        // Funció per carregar fitxers i reestructurar tota la info en un sol JSON.
        async carregarFitxers() {
            // Creem una promesa x cada fitxers, perquè es faci paral·lelament
            const promises = Array.from(this.fileList).map((file) => {
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = async (event) => {
                        const contingut = event.target.result;
                        console.log(file.tool)
                        console.log(file.name)
                        const parsedContent = await this.parseExcelJSON(contingut);
                        const contingutFormatted = this.transformarContingut(parsedContent, file.tool);
                        resolve(contingutFormatted);
                    };
                    reader.onerror = reject;
                    reader.readAsBinaryString(file.raw);
                });
            });
            try {
                // Recollim totes les promeses i les ajuntem en un sol JSON (info)
                const info = await Promise.all(promises);
                return info.reduce((acc, data) => ({ ...acc, ...data }), {});
            } catch (error) {
                console.error("Error carregant els fitxers:", error);
            }
        },
        async parseExcelJSON(contingut) {
            const XLSX = await import('xlsx'); 
            
            const workbook = XLSX.read(contingut, { type: 'binary' });
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];

            const data = {};

            // Extract headers from the first row
            const headers = [];
            for (let cell in worksheet) {
                const col = cell.replace(/[0-9]/g, '');
                const row = parseInt(cell.replace(/[A-Za-z]/g, ''), 10);

                if (row === 1) {
                    headers.push(worksheet[cell].v);
                }
            }

            Object.keys(worksheet).forEach((cell) => {
                const col = cell.replace(/[0-9]/g, '');
                const row = parseInt(cell.replace(/[A-Za-z]/g, ''), 10);

                // Skip header row
                if (row === 1) return;

                const value = worksheet[cell].v;

                const header = headers[col.charCodeAt(0) - 'A'.charCodeAt(0)];

                if (!data[header]) {
                    data[header] = {
                        count: 0,
                        total: 0,
                        value: null,
                    };
                }

                if (!isNaN(value)) {
                    // If the value is a number, update the total and count
                    data[header].total += parseFloat(value);
                    data[header].count += 1;
                } else if (data[header].count === 0) {
                    // If the value is not a number and it's the first non-numeric value, set it as the value
                    data[header].value = value;
                }
            });

            const result = {};

            Object.keys(data).forEach((key) => {
                if (data[key].count > 0) {
                    // If the column has numerical values, calculate the average
                    result[key] = data[key].total / data[key].count;
                } else {
                    // If the column has only text, use the first non-numeric value
                    result[key] = data[key].value;
                }
            });

            // Assign the resulting JSON to a variable
            const jsonResult = result;
            return jsonResult
        },
        transformarContingut(contingut, eina) {
            if (eina) {
                const dadesEina = this.eines.find(e => e.id = eina)
                const transformacionsMetriques = dadesEina.transformacionsMetriques
                const transformacionsInformacions = dadesEina.transformacionsInformacions
                return this.substituirContingut(contingut, {...transformacionsMetriques, ...transformacionsInformacions})
            } else return contingut
        },
        substituirContingut(contingut, transformacio) {
            let nouContingut = {}
            for (const clau in contingut) {
                if (transformacio[clau]) nouContingut[transformacio[clau]] = contingut[clau]
                else nouContingut[clau] = contingut[clau]
            }
            return nouContingut
        },
    },
    async mounted() {
        await this.refrescaEines();
    },
};
</script>

<style>
p {
    font-size: 18px
}
</style>