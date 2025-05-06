import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export default {
    /**
     * Generate a PDF report of the ROI analysis
     */
    async generatePDFReport(analysisData, elementId, fileName = 'roi-analysis-report.pdf') {
        try {
            // Get the container element with all the analysis data
            const element = document.getElementById(elementId);
            
            if (!element) {
                console.error('Element not found:', elementId);
                return;
            }
            
            // Create a clone of the element to avoid modifying the original
            const clonedElement = element.cloneNode(true);

            // Hide unnecessary elements
            const clonedExportButtonContainer = clonedElement.querySelector('.export-button-container');
            if (clonedExportButtonContainer) {
                clonedExportButtonContainer.style.display = 'none';
            }
            const clonedViewToggle = clonedElement.querySelector('.view-toggle');
            if (clonedViewToggle) {
                clonedViewToggle.style.display = 'none';
            }
            
            // Apply styles to prepare for PDF
            clonedElement.style.width = '1200px';
            clonedElement.style.padding = '20px';
            clonedElement.style.background = 'white';
            
            // Temporarily add to document but hide it
            clonedElement.style.position = 'absolute';
            clonedElement.style.left = '-9999px';
            document.body.appendChild(clonedElement);
            
            // Create and format the PDF title
            const titleElement = document.createElement('h1');
            titleElement.textContent = `ROI Analysis Report - ${analysisData.model_architecture_name} with ${analysisData.tactic_parameter_option_details?.tactic_name}`;
            titleElement.style.textAlign = 'center';
            titleElement.style.color = 'var(--gaissa_green)';
            titleElement.style.marginBottom = '20px';
            clonedElement.insertBefore(titleElement, clonedElement.firstChild);
            
            // Add report generation date
            const dateElement = document.createElement('p');
            dateElement.textContent = `Report generated on: ${new Date().toLocaleString()}`;
            dateElement.style.textAlign = 'right';
            dateElement.style.fontStyle = 'italic';
            dateElement.style.marginBottom = '30px';
            clonedElement.insertBefore(dateElement, titleElement.nextSibling);
            
            // Replace each chart container with its canvas image
            const chartContainers = clonedElement.querySelectorAll('.chart-container');
            
            for (let i = 0; i < chartContainers.length; i++) {
                const originalChartContainer = document.querySelectorAll('.chart-container')[i];
                
                if (!originalChartContainer) continue;
                
                try {
                    // Find the canvas within the chart container
                    const chartCanvas = originalChartContainer.querySelector('canvas');
                    if (chartCanvas) {
                        // Get the chart's image data
                        const chartImage = chartCanvas.toDataURL('image/png', 1.0);
                        
                        // Create an image element to replace the chart container
                        const chartImg = document.createElement('img');
                        chartImg.src = chartImage;
                        chartImg.style.width = '100%';
                        chartImg.style.maxHeight = '400px';
                        chartImg.style.objectFit = 'contain';
                        
                        // Replace the chart container in the clone with the image
                        const clonedChartContainer = chartContainers[i];
                        clonedChartContainer.innerHTML = '';
                        clonedChartContainer.appendChild(chartImg);
                    }
                } catch (err) {
                    console.error('Error capturing chart:', err);
                }
            }
            
            // Initialize PDF with A4 size
            const pdf = new jsPDF('p', 'pt', 'a4');
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = pdf.internal.pageSize.getHeight();
            
            try {
                const canvas = await html2canvas(clonedElement, {
                    scale: 4,
                    useCORS: true,
                    logging: false,
                    foreignObjectRendering: false,
                    removeContainer: true,
                });

                const imgData = canvas.toDataURL('image/jpeg', 1.0);

                const canvasOriginalWidth = canvas.width;    // Width of the canvas (in pixels)
                const canvasOriginalHeight = canvas.height;  // Height of the canvas (in pixels)

                const pdfPageWidth = pdf.internal.pageSize.getWidth();     // Width of the PDF page (in points)
                const pdfPageHeight = pdf.internal.pageSize.getHeight();   // Height of the PDF page (in points)

                // Calculate the scale ratio to fit the canvas width to the PDF page width
                // This ratio converts canvas pixel dimensions to PDF point dimensions for rendering
                const scaleToFitPdfWidth = pdfPageWidth / canvasOriginalWidth;

                // Calculate the dimensions of the image as it will be rendered on the PDF
                const imageWidthOnPdf = canvasOriginalWidth * scaleToFitPdfWidth;
                const imageHeightOnPdfTotal = canvasOriginalHeight * scaleToFitPdfWidth; // Total height the image would occupy if PDF page was infinitely tall

                // Calculate X offset for centering the image on the PDF page
                const imageXOffsetOnPdf = (pdfPageWidth - imageWidthOnPdf) / 2;

                let yPositionOfImageSegmentOnPdf = 0; // This will be the negative offset for subsequent pages
                let remainingImageHeightToPrint = imageHeightOnPdfTotal;

                // Add the first page/segment of the image
                pdf.addImage(
                    imgData,
                    'PNG',
                    imageXOffsetOnPdf,
                    yPositionOfImageSegmentOnPdf,
                    imageWidthOnPdf,
                    imageHeightOnPdfTotal,
                    'FAST',
                );

                remainingImageHeightToPrint -= pdfPageHeight; // Subtract one page height

                // Add new pages if content overflows
                while (remainingImageHeightToPrint > 0.01) {
                    yPositionOfImageSegmentOnPdf -= pdfPageHeight; // "Scroll" the image up by one page height
                    pdf.addPage();
                    pdf.addImage(
                        imgData,
                        'PNG',
                        imageXOffsetOnPdf,
                        yPositionOfImageSegmentOnPdf, // Negative offset shows the next part of the image
                        imageWidthOnPdf,
                        imageHeightOnPdfTotal,
                        'FAST',
                    );
                    remainingImageHeightToPrint -= pdfPageHeight;
                }

                pdf.save(fileName);
                document.body.removeChild(clonedElement);
                return true;

            } catch (error) {
                console.error('Error generating PDF from canvas:', error);
                document.body.removeChild(clonedElement);
                return false;
            }
        } catch (error) {
            console.error('Error in PDF generation service:', error);
            return false;
        }
    }
};