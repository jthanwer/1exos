import {
  required,
  min,
  min_value,
  max_value,
  email,
  integer,
  regex
} from 'vee-validate/dist/rules'
import { extend } from 'vee-validate'
import { setInteractionMode } from 'vee-validate'
import { localize } from 'vee-validate'
import fr from 'vee-validate/dist/locale/fr.json'

import usersService from '@/services/usersService'

localize('fr', fr)

setInteractionMode('lazy')

const isUnique = function(type) {
  return value =>
    new Promise(resolve => {
      const payload = {}
      payload[type] = value
      usersService.check_credentials(payload).then(data => {
        if (data['unique']) {
          return resolve({
            valid: true
          })
        }

        return resolve({
          valid: false
        })
      })
    })
}

const isVille = function() {
  return value =>
    new Promise(resolve => {
      fetch('data/villes.json')
        .then(r => r.json())
        .then(villes => {
          if (villes.includes(value)) {
            return resolve({
              valid: true
            })
          }

          return resolve({
            valid: false
          })
        })
    })
}

const isEtablissement = function() {
  return (value, { target }) =>
    new Promise(resolve => {
      fetch('data/etablissements.json')
        .then(r => r.json())
        .then(etablissements => {
          if (target && etablissements[target].includes(value)) {
            return resolve({
              valid: true
            })
          }

          return resolve({
            valid: false
          })
        })
    })
}

extend('required', {
  ...required,
  message: 'Ce champ est requis'
})

extend('prof', {
  ...regex,
  message:
    'Le nom ne doit contenir que des lettres et éventuellement des tirets.'
})

extend('integer', {
  ...integer,
  message: 'Le nombre doit être un entier'
})

extend('email', {
  ...email,
  message: "L'adresse e-mail n'est pas valide"
})

extend('min', {
  ...min,
  message: 'Ce champ doit contenir au moins {length} caractères'
})

extend('min_value', {
  ...min_value,
  message: 'Le nombre entré doit être supérieur ou égal à {min}'
})

extend('max_value', {
  ...max_value,
  message: 'Le nombre entré doit être inférieur ou égal à {max}'
})

extend('max_tirelire_value', {
  validate(value, { tirelire_avail, tirelire }) {
    if (value > tirelire) {
      return "Tu n'as pas assez de points dans ta tirelire"
    } else if (value > tirelire_avail) {
      return `Tu ne peux pas céder autant de points car tu as 
      déjà promis trop de points en échange de corrections.`
    } else {
      return true
    }
  },
  params: ['tirelire_avail', 'tirelire']
})

extend('unique_username', {
  validate: isUnique('username'),
  message: 'Ce pseudo est déjà pris par un autre utilisateur'
})

extend('unique_email', {
  validate: isUnique('email'),
  message: 'Cette adresse e-mail est déjà prise par un autre utilisateur'
})

extend('ville', {
  validate: isVille(),
  message: `Cette ville n'est pas référencée dans notre base de données.`
})

extend('etablissement', {
  params: ['target'],
  validate: isEtablissement(),
  message: `Cet établissement n'est pas référencé dans notre base de données.`
})

extend('same_password', {
  params: ['target'],
  validate(value, { target }) {
    return value === target
  },
  message: 'Les mots de passe ne correspondent pas'
})

extend('same_email', {
  params: ['target'],
  validate(value, { target }) {
    return value === target
  },
  message: 'Les adresses e-mail ne correspondent pas'
})
