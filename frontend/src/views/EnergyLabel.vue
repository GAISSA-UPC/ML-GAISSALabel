<template>

    <div>
        <iframe :src="pdfURL" type="application/pdf" width="100%" height="900px" />
    </div>
</template>

<script>
import trainings from '@/services/trainings'
export default {
    name: "EnergyLabel",
    data() {
        return {
            pdfURL: ""
        };
    },
    methods: {
        async aconseguirPDF() {
            // Aconseguim PDF en base64 de l'API
            const response = await trainings.retrieve(1, 1)
            const pdfBase64 = response.data['energy_label']
            console.log("pdfBase64")
            console.log(pdfBase64)

            // Convertim base64 a binari
            const binaryData = atob(pdfBase64);

            // Creem Blob a partir del binari
            const blob = new Blob([binaryData], { type: "application/pdf" });

            // Creem una URL pel Blob
            this.pdfURL = URL.createObjectURL(blob);
            console.log(this.pdfURL)
            console.log("hola")
        }
    },
    async mounted() {
        await this.aconseguirPDF();
    },
    beforeUnmount() {
        // Revoke the URL object to free up memory when the component is destroyed
        if (this.pdfURL) {
            URL.revokeObjectURL(this.pdfURL);
        }
    }
};
</script>