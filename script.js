// small helpers
document.getElementById('year').textContent = new Date().getFullYear();

// Optional: client-side form success redirect (Netlify will POST and return default page).
// You can customize to show a message instead of leaving the page.
document.querySelectorAll('form[data-netlify]').forEach(form=>{
  form.addEventListener('submit', function(){
    // Optionally show a toast or disable submit here.
  });
});
