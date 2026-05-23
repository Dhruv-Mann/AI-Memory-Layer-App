import { browser } from '$app/environment';

/**
 * Initializes paint performance observation to measure First Contentful Paint (FCP).
 * Fires warning logs if FCP exceeds the 1.5-second target threshold.
 */
export function initPerformanceMonitoring() {
	if (!browser) return;

	try {
		// Use standard PerformanceObserver to capture FCP metric
		const observer = new PerformanceObserver((list) => {
			for (const entry of list.getEntries()) {
				if (entry.name === 'first-contentful-paint') {
					const fcp = entry.startTime;
					console.log(`[Performance Metrics] First Contentful Paint: ${fcp.toFixed(2)}ms`);
					
					if (fcp > 1500) {
						console.warn(
							`[Performance Metrics] First Contentful Paint (${fcp.toFixed(2)}ms) exceeds the target limit of 1500ms!`
						);
					} else {
						console.log(
							`[Performance Metrics] Target met: FCP is under 1.5 seconds.`
						);
					}
				}
			}
		});

		// Start observing paint events
		observer.observe({ type: 'paint', buffered: true });
	} catch (e) {
		console.warn('[Performance Metrics] PerformanceObserver paint metrics are not supported in this browser.');
	}
}
