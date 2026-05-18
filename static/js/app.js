'use strict';


/** Select-first “Select All” option mirrors legacy behaviour */


document.addEventListener('DOMContentLoaded', () => {


  const select = document.querySelector('select[name="wheel_results"]');




  if (!select) {


    return;


  }







  select.addEventListener('change', () => {





    const options = Array.from(select.options);





    if (options.length > 0 && options[0].selected) {


      options.forEach((opt) => {


        opt.selected = true;





      });


    }


  });






});




