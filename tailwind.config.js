/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    darkMode: 'class',
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        './**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!./**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // './**/*.js',
        /* JS 3: Process specific JavaScript files in the project. */
        // './**/static/js/main.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // './**/*.py'
    ],
    // * ---------------- CLASES INCLUDED MANUALLY ----------------
    safelist: [
        'bg-blue-100', 'bg-gray-100', 'bg-indigo-100', 'bg-teal-600', 'bg-violet-100', 'dark:bg-blue-600',
        'dark:bg-gray-600', 'dark:bg-indigo-800', 'dark:bg-violet-800', 'dark:hover:bg-gray-600',
        'dark:hover:text-white', 'flex', 'flex-none', 'font-normal', 'h-10', 'h-full', 'hover:bg-gray-100',
        'items-center', 'md:h-fit', 'md:ml-28', 'md:mr-28', 'md:mx-32', 'md:w-full', 'ml-8', 'mr-2', 'mr-8',
        'p-2', 'p-3', 'p-4', 'rounded-full', 'rounded-lg', 'shrink-0', 'text-center', 'underline', 'user-chat-entry',
        'w-10', 'w-fit',
    ],
    // * ----------------------------------------------------------
    theme: {
        extend: {},
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('tailwindcss'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
        require('autoprefixer'),
    ],
}
