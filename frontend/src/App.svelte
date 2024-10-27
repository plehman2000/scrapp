<svelte:options runes={false} />

<script>
	let name = "Svelte";
	let img_src = "assets/nigga.png";

	let claim = $state("");
</script>

<h1>Hello {name}</h1>
<img src={img_src} alt="gay" />

<input bind:value={claim} placeholder="Enter your claim here!" />
