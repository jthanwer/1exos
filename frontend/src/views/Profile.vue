pychar<template>
<div id="profile-container"
     class="container is-fluid">
  <div class="columns is-gapless"
       style="min-height: 800px;">
    <div class="column is-4 card">
      <div class="card-content">
        <b-menu>
          <b-menu-list label="Profil">
            <b-menu-item icon="account"
                         :active="isActive"
                         @click="selected = 1"
                         label="Identité">
            </b-menu-item>
            <b-menu-item icon="book"
                         @click="selected = 2"
                         label="Scolarité">
            </b-menu-item>
            <b-menu-item icon="lock-reset"
                         @click="selected = 3"
                         label="Mot de passe">
            </b-menu-item>
          </b-menu-list>
        </b-menu>
      </div>
    </div>

    <div class="column is-8 card">
      <div v-if="selected === 1">
        <header class="card-header is-centered">
          <p class="card-header-title has-background-primary has-text-white is-size-3">
            Identité
          </p>
        </header>
        <div class="card-content">
          <div v-if="user"
               class="content">
            <div class="columns has-text-centered">
              <div class="column is-half">
                <div class="box">
                  <!-- <b-button @click="
                        form_user_active['username'] = !form_user_active['username']"
                            :type="{ 'is-primary': form_user_active['username'] }"
                            icon-left="pencil"
                            :native-value="true"
                            class="mb-3 is-pulled-right">
                  </b-button> -->
                  <strong class="heading">Pseudo</strong>
                  <p class="title is-5">{{ user.username }}</p>
                  <ValidationObserver ref="username">
                    <form v-if="form_user_active['username']"
                          @submit.prevent="validateForm('username')">
                      <ValidationProvider slim rules="required|unique_username"
                                          v-slot="{ errors, valid }">
                        <b-field position="is-centered"
                                 grouped>
                          <b-field :message="errors"
                                   :type="{
                                'is-danger': errors[0],
                                'is-success': valid
                              }">
                            <b-input v-model="form_user['username']"
                                     placeholder="Nouveau pseudo..."></b-input>
                          </b-field>
                          <b-button @click="validateForm('username')"
                                    class="mb-3 is-pulled-right"
                                    type="is-success">Valider</b-button>
                        </b-field>
                      </ValidationProvider>
                    </form>
                  </ValidationObserver>
                </div>
              </div>
              <div class="column is-half">
                <div class="box">
                  <!-- <b-button @click="form_user_active['email'] = !form_user_active['email']"
                            :type="{ 'is-primary': form_user_active['email'] }"
                            icon-left="pencil"
                            :native-value="true"
                            class="mb-3 is-pulled-right">
                  </b-button> -->
                  <strong class="heading">Adresse e-mail</strong>
                  <p class="title is-5">{{ user.email }}</p>
                  <ValidationObserver ref="email">
                    <form v-if="form_user_active['email']"
                          @submit.prevent="validateForm('email')">
                      <ValidationProvider slim rules="required|email|unique_email"
                                          v-slot="{ errors, valid }">
                        <b-field position="is-centered"
                                 grouped>
                          <b-field :message="errors"
                                   :type="{
                                'is-danger': errors[0],
                                'is-success': valid
                              }">
                            <b-input v-model="form_user['email']"
                                     placeholder="Nouvelle adresse e-mail..."></b-input>
                          </b-field>
                          <b-button @click="validateForm('email')"
                                    class="mb-3 is-pulled-right"
                                    type="is-success">Valider</b-button>
                        </b-field>
                      </ValidationProvider>
                    </form>
                  </ValidationObserver>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="selected === 2">
        <header class="card-header">
          <p class="card-header-title has-background-primary has-text-white is-size-3">
            Scolarité
          </p>
        </header>
        <div class="card-content">
          <div v-if="user"
               class="content">
            <div class="columns is-multiline has-text-centered">
              <div class="column is-half">
                <div class="box">
                  <b-button @click="
                        form_user_active['classe'] = !form_user_active['classe']"
                            :type="{ 'is-primary': form_user_active['classe'] }"
                            icon-left="pencil"
                            :native-value="true"
                            class="mb-3 is-pulled-right">
                  </b-button>
                  <strong class="heading">Niveau</strong>
                  <p class="title is-5">{{ classes[user.classe] }}</p>
                  <ValidationObserver ref="classe">
                    <form v-if="form_user_active['classe']"
                          @submit.prevent="validateForm('classe')">
                      <ValidationProvider slim rules="required"
                                          v-slot="{ errors, valid }">
                        <b-field position="is-centered"
                                 grouped>
                          <b-field :message="errors"
                                   :type="{
                                'is-danger': errors[0],
                                'is-success': valid
                              }">
                            <b-select v-model="form_user['classe']"
                                      placeholder="Choisis ta classe...">
                              <option v-for="(value, key) in classes"
                                      :value="key">{{ value }}</option>
                            </b-select>
                          </b-field>
                          <b-button @click="validateForm('classe')"
                                    class="mb-3 is-pulled-right"
                                    type="is-success">Valider</b-button>
                        </b-field>
                      </ValidationProvider>
                    </form>
                  </ValidationObserver>
                </div>
              </div>
              <div class="column is-half">
                <div class="box">
                  <b-button @click="form_user_active['prof'] = !form_user_active['prof']"
                            :type="{ 'is-primary': form_user_active['prof'] }"
                            icon-left="pencil"
                            :native-value="true"
                            class="mb-3 is-pulled-right">
                  </b-button>
                  <strong class="heading">Professeur de méthématiques</strong>
                  <p class="title is-5">
                    <span class="mr-1">{{
                        user.prefix_prof ? "M." : "Mme"
                      }}</span>
                    <span>{{ user.nom_prof }}</span>
                  </p>
                  <ValidationObserver ref="prof">
                    <form v-if="form_user_active['prof']"
                          @submit.prevent="validateForm('prof')">
                      <b-field grouped>
                        <ValidationProvider slim rules="required"
                                            v-slot="{ errors, valid }">
                          <b-field :message="errors"
                                   :type="{
                                'is-danger': errors[0],
                                'is-success': valid
                              }">
                            <b-select v-model="form_user['prefix_prof']"
                                      placeholder="M. ou Mme">
                              <option :value="true">M.</option>
                              <option :value="false">Mme</option>
                            </b-select>
                          </b-field>
                        </ValidationProvider>
                        <ValidationProvider slim rules="required"
                                            v-slot="{ errors, valid }">
                          <b-field :message="errors"
                                   :type="{
                                'is-danger': errors[0],
                                'is-success': valid
                              }">
                            <b-input v-model="form_user['nom_prof']"
                                     type="text"
                                     placeholder="Dupont">
                            </b-input>
                          </b-field>
                        </ValidationProvider>

                        <b-button @click="validateForm('prof')"
                                  class="mb-3 is-pulled-right"
                                  type="is-success">Valider</b-button>
                      </b-field>
                    </form>
                  </ValidationObserver>
                </div>
              </div>
              <div class="column is-12">
                <div class="box">
                  <b-button @click="
                        form_user_active['ville_etablissement'] = !form_user_active['ville_etablissement']"
                            :type="{ 'is-primary': form_user_active['ville_etablissement']}"
                            icon-left="pencil"
                            :native-value="true"
                            class="mb-3 is-pulled-right">
                  </b-button>
                  <strong class="heading">Ville</strong>
                  <p class="title is-5">{{ user.ville_etablissement }}</p>
                  <ValidationObserver ref="ville_etablissement">
                    <form v-if="form_user_active['ville_etablissement']"
                          @submit.prevent="validateForm('ville_etablissement')">
                      <ValidationProvider slim rules="required"
                                          v-slot="{ errors, valid }">
                        <b-field position="is-centered"
                                 grouped>
                          <b-field :message="errors"
                                   :type="{
                                'is-danger': errors[0],
                                'is-success': valid
                              }">
                            <b-autocomplete expanded
                                            v-model="ville_input"
                                            placeholder="Cherche ta ville..."
                                            :data="ville_items"
                                            keep-first>
                              <template slot="empty">
                                <span v-if="ville_input.length > 3">Aucun résultat</span>
                                <span v-else>Tapes au moins 3 caractères</span>
                              </template>
                            </b-autocomplete>
                          </b-field>
                          <b-button @click="validateForm('ville_etablissement')"
                                    class="mb-3 is-pulled-right"
                                    type="is-success">Valider</b-button>
                        </b-field>
                      </ValidationProvider>
                    </form>
                  </ValidationObserver>
                </div>
              </div>
              <div class="column">
                <div class="box">
                  <b-button @click="
                        form_user_active['nom_etablissement'] = !form_user_active['nom_etablissement']"
                            :type="{
                        'is-primary': form_user_active['nom_etablissement']
                      }"
                            icon-left="pencil"
                            :native-value="true"
                            class="mb-3 is-pulled-right">
                  </b-button>
                  <strong class="heading">Établissement</strong>
                  <p class="title is-5">{{ user.nom_etablissement }}</p>
                  <ValidationObserver ref="nom_etablissement">
                    <form v-if="form_user_active['nom_etablissement']"
                          @submit.prevent="validateForm('nom_etablissement')">
                      <ValidationProvider slim rules="required"
                                          v-slot="{ errors, valid }">
                        <b-field grouped
                                 :message="errors"
                                 :type="{
                                'is-danger': errors[0],
                                'is-success': valid
                              }">
                          <b-autocomplete expanded
                                          v-model="etablissement_input"
                                          :loading="autocomplete_loading"
                                          placeholder="Cherche ton établissement..."
                                          :data="etablissement_items"
                                          keep-first>
                            <template slot="empty">
                              Aucun résultat
                            </template>
                          </b-autocomplete>
                          <b-button @click="validateForm('nom_etablissement')"
                                    class="mb-3 is-pulled-right"
                                    type="is-success">Valider</b-button>
                        </b-field>

                      </ValidationProvider>
                    </form>
                  </ValidationObserver>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="selected === 3">
        <header class="card-header">
          <p class="card-header-title has-background-primary has-text-white is-size-3">
            Mot de passe
          </p>
        </header>
        <ValidationObserver ref="change_password">
          <form class="card-content"
                @submit.prevent="changePassword()">
            <b-field grouped>
              <ValidationProvider slim rules="required"
                                  v-slot="{ errors, valid }">
                <b-field label="Ton mot de passe actuel"
                         :message="errors"
                         :type="{ 'is-danger': errors[0], 'is-success': valid }">
                  <b-input v-model="form_password.old_password"
                           type="password"
                           placeholder="Mot de passe actuel">
                  </b-input>
                </b-field>
              </ValidationProvider>
            </b-field>
            <b-field grouped>
              <ValidationProvider slim rules="required|min:6"
                                  name="new_password"
                                  v-slot="{ errors, valid }">
                <b-field label="Ton nouveau mot de passe"
                         :message="errors"
                         :type="{ 'is-danger': errors[0], 'is-success': valid }">
                  <b-input v-model="form_password.new_password"
                           type="password"
                           placeholder="Nouveau mot de passe"></b-input>
                </b-field>
              </ValidationProvider>
              <ValidationProvider slim rules="required|same_password:@new_password"
                                  v-slot="{ errors, valid }">
                <b-field label="Confirmation"
                         :message="errors"
                         :type="{ 'is-danger': errors[0], 'is-success': valid }">
                  <b-input v-model="form_password.new_password_confirm"
                           type="password"
                           @keydown.enter="validate"
                           placeholder="Retape ton mot de passe..."></b-input>
                </b-field>
              </ValidationProvider>
            </b-field>

            <button class="button is-primary is-fullwidth"
                    type="submit">
              Valider
            </button>
          </form>
        </ValidationObserver>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { mapState } from "vuex";
import { ValidationObserver, ValidationProvider } from "vee-validate";
import usersService from "@/services/usersService";
import classes from "@/data/classes.json";
export default {
  name: "Profile",
  components: {
    ValidationObserver,
    ValidationProvider
  },
  data() {
    return {
      classes: classes,

      selected: 2,
      isActive: true,
      password: null,
      form_user_active: {
        username: false,
        email: false,
        classe: false,
        ville_etablissement: false,
        nom_etablissement: false,
        prof: false
      },
      form_user: {
        username: null,
        email: null,
        classe: null,
        ville_etablissement: null,
        nom_etablissement: null,
        prefix_prof: null,
        nom_prof: null
      },
      form_password: {
        old_password: null,
        new_password: null,
        new_password_confirm: null
      },

      villes: [],
      ville_items: [],
      ville_input: "",
      etablissements: [],
      etablissement_items: [],
      etablissement_input: "",
      autocomplete_loading: false,
    };
  },
  created() {
    fetch('data/villes.json')
      .then(r => r.json())
      .then(json => { this.villes = json })
    fetch('data/etablissements.json')
      .then(r => r.json())
      .then(json => { this.etablissements = json })
  },
  computed: {
    ...mapState("authentication", ["user"])
  },
  methods: {
    changePassword() {
      this.$refs.change_password.validate().then(success => {
        if (!success) {
          return;
        }
        this.change_password_loading = true;
        usersService.change_password(this.form_password)
          .then(() => {
            this.form_password = {
              old_password: "",
              new_password: "",
              new_password_confirm: ""
            };
            this.$buefy.toast.open({
              duration: 5000,
              message: `Ton mot de passe a été modifé avec succès.
            Utilise maintenant ce mot de passe pour tes futures connexions.`,
              type: "is-success"
            });
            this.change_password_loading = false;
            this.$refs.change_password.reset();
          })
          .catch(err => {
            let status = err.response.status;
            let message = `Un problème est survenu... Réessaye plus tard.`;
            switch (status) {
              case 400:
                message = `Un problème est survenu... Vérifie les informations fournies.`;
                break;
              case 401:
                message = `Ta session est expirée, reconnecte-toi pour continuer.`;
                break;
              case 406:
                message = `Le mot de passe actuel donné est invalide.`;
                break;
              default:
                message = `Un problème est survenu... Réessaye plus tard.`;
            }
            this.$buefy.toast.open({
              duration: 5000,
              message: message,
              type: "is-danger"
            });
            this.change_password_loading = false;
          });
      });
    },
    validateForm(element) {
      this.form_user["ville_etablissement"] = this.ville_input;
      this.form_user["nom_etablissement"] = this.etablissement_input;
      this.$refs[element].validate().then(success => {
        if (!success) {
          return;
        }
        // If form is valid
        let payload = {};
        // Prof is split in two parts
        if (element == "prof") {
          payload["prefix_prof"] = this.form_user["prefix_prof"];
          payload["nom_prof"] = this.form_user["nom_prof"];
          this.updateProfile(payload, element);
        }
        // Username and email require password
        else if (["username", "email"].includes(element)) {
          payload[element] = this.form_user[element];
          this.askForPassword(payload, element);
        }
        // Else is basic
        else {
          payload[element] = this.form_user[element];
          this.updateProfile(payload, element);
        }
      });
    },
    askForPassword(payload, element) {
      this.$buefy.dialog.prompt({
        message: `Rentre ton mot de passe :`,
        type: "is-primary",
        inputAttrs: {
          type: "password",
          placeholder: "Ton mot de passe..."
        },
        cancelText: "Annuler",
        confirmText: "Valider",
        trapFocus: true,
        onConfirm: value => {
          payload["password"] = value;
          this.updateProfile(payload, element);
        }
      });
    },
    updateProfile(payload, element) {
      usersService
        .update_profile(this.user.pk, payload)
        .then(data => {
          this.form_user_active[element] = false;
          this.$buefy.toast.open({
            duration: 5000,
            message: `Ton profil a été mis à jour avec succès`,
            type: "is-success"
          });
          let updated_user = Object.assign(this.user, data);
          this.$store.dispatch(
            "authentication/updateProfileUser",
            updated_user
          );
        })
        .catch(err => {
          let status = err.response.status;
          let message = `Un problème est survenu... Réessaye plus tard.`;
          switch (status) {
            case 401:
              message = `Ta session est expirée, reconnecte-toi pour continuer.`;
              break;
            case 406:
              message = `Le mot de passe donné est invalide.`;
              break;
            default:
              message = `Un problème est survenu... Réessaye plus tard.`;
          }
          this.$buefy.toast.open({
            duration: 5000,
            message: message,
            type: "is-danger"
          });
        });
    },
    filterVilles(v) {
      this.ville_items = this.villes.filter(object => {
        return (
          (object || "")
          .toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .indexOf(
            (v || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
          ) > -1
        );
      });
    },
    filterEtablissements(v) {
      this.etablissement_items = this.etablissements[this.user.ville_etablissement]
        .filter(object => {
          return (
            (object || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .indexOf(
              (v || "")
              .toLowerCase()
              .normalize("NFD")
              .replace(/[\u0300-\u036f]/g, "")
            ) > -1
          );
        });
    },
  },
  watch: {
    ville_input: function(input) {
      input && input.length > 2 && this.filterVilles(input);
    },
    etablissement_input: function(input) {
      input && this.filterEtablissements(input);
    }
  }
};
</script>

<style scoped>
</style>
