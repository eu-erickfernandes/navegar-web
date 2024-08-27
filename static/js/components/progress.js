const progressContainers = document.querySelectorAll('[data-progress-total]')

if (progressContainers.length)
    progressContainers.forEach((container) => {
        const total = container.getAttribute('data-progress-total')

        const bar = container.querySelector('[data-progress-bar]')
        const totalProgress = bar.getAttribute('data-progress-bar')

        const barWidth = Math.round(100 * parseFloat(totalProgress) / parseFloat(total))
        bar.style.width = barWidth <= 100 ? `${barWidth}%` : '100%'
    })