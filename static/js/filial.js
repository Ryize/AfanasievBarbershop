document.getElementById('branchSelect').addEventListener('change', function() {
            const selectedValue = this.value;
            if (selectedValue) {
                let currentUrl = window.location.href;
                let urlParts = currentUrl.split('/');
                urlParts[-2] = selectedValue;
                window.location.href = urlParts.join('/');
            }
        });