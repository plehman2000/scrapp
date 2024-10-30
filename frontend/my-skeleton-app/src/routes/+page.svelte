<script>
	async function pingAPI() {
		try {
			const response = await fetch('/api/ping');
			const data = await response.json();
			resultText = `API response: ${data.message}`;
			showResult = true;
			inputText = '';
		} catch (error) {
			console.error('Error:', error);
		}
	}

	let inputText = '';
	let resultText = '';
	let showResult = false;
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center"></div>
	<div class="flex flex-row">
		<input
			class="input"
			title="Input (text)"
			type="text"
			placeholder="input text"
			bind:value={inputText}
		/>
		<button
			type="button"
			class="btn variant-filled bg-blue-500 hover:bg-blue-600 text-white"
			on:click={pingAPI}>Submit</button
		>
	</div>
	{#if showResult}
		<div class="mt-4">{resultText}</div>
	{/if}
</div>

<style lang="postcss">
	figure {
		@apply flex relative flex-col;
	}
	figure svg,
	.img-bg {
		@apply w-64 h-64 md:w-80 md:h-80;
	}
	.img-bg {
		@apply absolute z-[-1] rounded-full blur-[50px] transition-all;
		animation:
			pulse 5s cubic-bezier(0, 0, 0, 0.5) infinite,
			glow 5s linear infinite;
	}
</style>
