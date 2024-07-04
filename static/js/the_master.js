document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.master').forEach(function(element) {
                element.addEventListener('click', function(event) {
                    event.preventDefault();
                    let branchId = this.dataset.branchid;
                    let masterId = this.dataset.masterid;
                    const url = `/admins/master/${branchId}/${masterId}`;
                    window.location.href = url;
                });
            });
        });