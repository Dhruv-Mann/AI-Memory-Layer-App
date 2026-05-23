/**
 * Reusable utility to export SVG-based charts to SVG or PNG format.
 */
export function exportChart(
	containerElement: HTMLElement,
	fileName: string,
	format: 'svg' | 'png' = 'svg'
) {
	if (!containerElement) return;

	// Find the first SVG element inside the container
	const svgElement = containerElement.querySelector('svg');
	if (!svgElement) {
		console.error('No SVG element found for export');
		return;
	}

	try {
		// Serialize SVG to XML string
		const serializer = new XMLSerializer();
		
		// Add standard XML namespaces if not present
		if (!svgElement.getAttribute('xmlns')) {
			svgElement.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
		}

		// Inject active styling rules into SVG for accurate standalone rendering
		const clonedSvg = svgElement.cloneNode(true) as SVGElement;
		
		// Inline styling if needed
		clonedSvg.setAttribute('style', 'background-color: var(--bg-primary, #ffffff); font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;');

		const svgString = serializer.serializeToString(clonedSvg);

		if (format === 'svg') {
			const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
			const url = URL.createObjectURL(blob);
			downloadFile(url, `${fileName}.svg`);
		} else if (format === 'png') {
			// Get SVG size boundaries
			const rect = svgElement.getBoundingClientRect();
			const width = rect.width || 600;
			const height = rect.height || 300;

			// Prepare image element to draw onto canvas
			const img = new Image();
			const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
			const url = URL.createObjectURL(blob);

			img.onload = () => {
				const canvas = document.createElement('canvas');
				// Increase DPI for crisp text scaling
				const scale = window.devicePixelRatio || 2;
				canvas.width = width * scale;
				canvas.height = height * scale;

				const ctx = canvas.getContext('2d');
				if (ctx) {
					ctx.scale(scale, scale);
					// Draw background fill
					ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-primary').trim() || '#ffffff';
					ctx.fillRect(0, 0, width, height);
					
					ctx.drawImage(img, 0, 0, width, height);

					const pngUrl = canvas.toDataURL('image/png');
					downloadFile(pngUrl, `${fileName}.png`);
				}
				URL.revokeObjectURL(url);
			};

			img.src = url;
		}
	} catch (err) {
		console.error('Failed to export chart:', err);
	}
}

function downloadFile(url: string, name: string) {
	const a = document.createElement('a');
	a.href = url;
	a.download = name;
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	URL.revokeObjectURL(url);
}
