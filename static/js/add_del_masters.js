document.addEventListener('DOMContentLoaded', (event) => {
                const button_add_mon = document.querySelectorAll('.but_add_work_mon');
                const button_add_eve = document.querySelectorAll('.but_add_work_eve');
                const button_del_mon = document.querySelectorAll('.but_del_work_mon');
                const button_del_eve = document.querySelectorAll('.but_del_work_eve');

                button_add_mon.forEach(button => {
                    button.addEventListener('click', () => {
                        const chairNum = button.getAttribute('data-chair-num');
                        const form = document.getElementById(`work_mon_${chairNum}`);
                        form.submit();
                    });
                });

                button_add_eve.forEach(button => {
                    button.addEventListener('click', () => {
                        const chairNum = button.getAttribute('data-chair-num');
                        const form = document.getElementById(`work_eve_${chairNum}`);
                        form.submit();
                    });
                });
                button_del_mon.forEach(button => {
                    button.addEventListener('click', () => {
                        const chairNum = button.getAttribute('data-chair-num');
                        const form = document.getElementById(`work_mon_${chairNum}`);
                        form.submit();
                    });
                });

                button_del_eve.forEach(button => {
                    button.addEventListener('click', () => {
                        const chairNum = button.getAttribute('data-chair-num');
                        const form = document.getElementById(`work_eve_${chairNum}`);
                        form.submit();
                    });
                });
            })