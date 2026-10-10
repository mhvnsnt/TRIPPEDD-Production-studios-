'use strict';
// TRIPPEDD lower-third extension proof: announces itself on load and
// keeps a Replicant with the current lower-third payload.
module.exports = function (nodecg) {
	nodecg.log.info('trippedd-lowerthird extension loaded (wave39 proof)');
	const lowerThird = nodecg.Replicant('lowerThird', {
		defaultValue: { name: 'ASHES', title: 'TRIPPEDD STATION IDENT' }
	});
	lowerThird.on('change', (nv) => {
		nodecg.log.info('lowerThird replicant updated: ' + JSON.stringify(nv));
	});
};
