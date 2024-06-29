document.addEventListener('DOMContentLoaded', function() {
    const mastersButton = document.getElementById('all_masters');
    const branchSelect = document.getElementById('branchSelect');
    mastersButton.addEventListener('click', function() {
        const selectedBranch = branchSelect.value;
        if (selectedBranch) {
            window.location.href = `/admins/all_masters/${selectedBranch}/`;
        }
    });
});