<template>

    <div>
        <embed :src="pdfURL" type="application/pdf" width="100%" height="600px" />
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
            const pdfBase64 = await trainings.retrieve(1, 1)

            // Convertim base64 a binari
            const binaryData = atob(pdfBase64);

            // Creem Blob a partir del binari
            const blob = new Blob([binaryData], { type: "application/pdf" });

            // Creem una URL pel Blob
            this.pdfURL = URL.createObjectURL(blob);
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