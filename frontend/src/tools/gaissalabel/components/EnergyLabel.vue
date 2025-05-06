<template>

    <div>
        <iframe :src="pdfURL" type="application/pdf" width="100%" height="600px"/>
    </div>
</template>

<script>
export default {
    name: "EnergyLabel",
    props: {
        pdfBase64: {
            required: true,
            type: String,
            validator(value) {
                return value !== null && value !== "";
            }
        }
    },
    data() {
        return {
            pdfURL: ""
        };
    },
    methods: {
        async aconseguirPDF() {
            // Convertim base64 a binari
            const binaryData = atob(this.pdfBase64);

            // Creem Blob a partir del binari
            const blob = new Blob([binaryData], { type: "application/pdf" });

            // Creem una URL pel Blob
            this.pdfURL = URL.createObjectURL(blob);
        }
    },
    watch: {
        pdfBase64() {
            this.aconseguirPDF()
        },
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